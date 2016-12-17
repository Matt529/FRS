from typing import List, Dict
from collections import OrderedDict

import os
import json
import subprocess
import re

from django.core.management.base import BaseCommand

from FRS.config._cfg import ConfigValue
from FRS.config.api import names as resnames
from FRS.config import base
from tastypie.resources import Resource
from tastypie.fields import NOT_PROVIDED

from funcy.funcs import map, partial, compose, reduce, rpartial
from funcy.types import isa
from funcy.colls import select
from funcy.seqs import flatten
from funcy.strings import str_join

from util.strutils import fqn

import api

META_IDENTIFIER_NAME = 'generate_clientside_interface'
META_SCHEMA_NAME = 'clientside_schema_name'

OUTPUT_COMMENT = "Auto-generated by '%s', modify with care." % os.path.basename(__file__)[:-3]
SCHEMA_DIR = os.path.join(base.BASE_DIR(), 'static', 'global', 'schemas')

"""
    Regular expression for matching an attribute declaration in a model docstring. This include the type override
    @command. It matches strings of the form:
    
    :attr <name>[ {@type}|{@collection[type]}]: <documentation>
    
    The regexp groups as is are:
    
        1. Attribute Name
        2. Type Override @command (including brackets)
        3. Documentation Text
"""
RE_ATTRIBUTE_DEF = re.compile(r':attr\s+([^\d\W]\w*)\s*(\{@[^\d\W].*\})?:\s*([^:]*)', re.MULTILINE)

"""
    Matches a type override @command of the form:

    @<collection|coll|list|set|array|...>[<type>]
    
    Which captures a single group:
    
        1. The Componenet Type (i.e. if the command is @array[int], Group 1 is 'int')
        
"""
RE_ARRAY_TYPE_OVERRIDE = re.compile(r'(collection|coll|array|arr|list|set)\[([^\d\W]\w*)\]')

"""
    Matches a type override @command of the form:
    
    @<type>
    
    Which captures a single group:
    
    1. The Type (i.e. if the command is @int, Group 1 is 'int')
    
    Very similar to the Array Type Regexp but with a @ at the front to differentiate the two explicitly.
"""
RE_TYPE_OVERRIDE = re.compile(r'@([^\d\W]\w*)')

"""
Valid type override and their mapped Schema counterparts.
"""
TYPE_OVERRIDES = {
    'int': 'integer',
    'integer': 'integer',
    'float': 'number',
    'number': 'number',
    'str': 'string',
    'string': 'string',
}

DEFAULT_TYPE_OVERRIDE = 'any'

# Funcy Function Definitions:

resource_transformer = lambda api_obj: partial(map, api_obj.canonical_resource_for)
to_cv_values = partial(map, lambda cv: cv.value)
select_config = partial(select, isa(ConfigValue))
is_class = isa(type)

get_correct_meta = lambda o: o.Meta if is_class(o) else o._meta
is_marked = lambda o: (lambda x: hasattr(x, META_IDENTIFIER_NAME) and getattr(x, META_IDENTIFIER_NAME))(get_correct_meta(o))
select_with_identifier = partial(select, is_marked)

to_schema_name = lambda o: (lambda x: getattr(x, META_SCHEMA_NAME, x.resource_name))(get_correct_meta(o))
to_fqns = partial(map, fqn)

commas = partial(str_join, ', ')
str_drop_empty = partial(select, lambda s: s != '')
str_trim = lambda s: s.strip()
str_split = lambda on: (lambda s: s.split(on))
str_split_pattern = lambda pattern: (lambda s: re.split(pattern, s))
str_split_newline = str_split_pattern(r'\r?\n')
char_arr_to_string = partial(str_join, '')

space_out_title_case = compose(lambda s: s.lstrip(), char_arr_to_string, flatten, rpartial(partial(reduce, lambda left, right: left + (' ' + right if right.isupper() else right)), ''))
substitute_char = lambda target, replacement: partial(map, lambda c: replacement if c == target else c)
lowercase = partial(map, lambda c: c.lower())
slugify = compose(char_arr_to_string, substitute_char(' ', '-'), space_out_title_case)

normalize_whitespace = compose(partial(str_join, '\n '), str_drop_empty, partial(map, str_trim), str_split_newline)


class NO_TYPE:
    pass


class FieldDescriptor(object):
    def __init__(self, desc: str, is_array: bool = False, type_override=NO_TYPE):
        self.description = desc
        self.is_array = is_array
        self.type_override = type_override
    
    def __str__(self):
        return "FieldDesc[is_arr=%s, type=%s" % (self.is_array, self.type_override)
    
    def __repr__(self):
        return str(self)

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('api_name', metavar="API_VERSION", type=str, help="The Name of the API Version (e.g. v1)")
        parser.add_argument('--no-build', dest='build', action='store_false', help="Do not build d.ts files, the schemas will still be built.")
    
    def handle(self, *args, **options):
        api_name = options.pop('api_name')

        frsapi = api.FRSApi.get_instance(api_name)
        
        # Get all Resources known at configuration
        possible_resources = resource_transformer(frsapi)(to_cv_values(select_config([*resnames.__dict__.values()])))
        
        # Get Resources marked as 'generatable' with the meta flag existing and set to True
        resources = select_with_identifier(possible_resources)          # type: List[Resource]

        difference = select(lambda x: x not in resources, possible_resources)
        if len(difference) > 0:
            print("Skipping %s since their %s meta flag is either missing or false." % (commas(to_fqns(difference)), META_IDENTIFIER_NAME))
        
        print("Performing Interface Generation for: %s" % (commas(to_fqns(resources))))
        
        # Generate schema files, tastypie's build_schema to do the heavy lifting, most of the work done in this
        # command is cleaning up and selecting what we need from the tastypie schema.
        for resource in resources:
            print("\n%s:" % fqn(resource))
            print("=============================================")
            print("Preparing schema...")
            raw_schema = resource.build_schema()
            schema = self.process_tastypie_schema(resource, raw_schema)
            schema_path = os.path.join(SCHEMA_DIR, '%s-schema.json' % slugify(schema['title']))
            print("Writing out schema to %s..." % schema_path)
            with open(schema_path, 'w') as schema_file:
                json.dump(schema, schema_file, indent=4)
            print("=============================================")
        
        # Execute schema -> d.ts build if --no-build flag is not specified
        if options['build']:
            print("\nGenerating d.ts files via gulp...\nGulp Output:")
            rc = subprocess.call("gulp generateInterfaces", shell=True)
            if rc != 0:
                print("Failed to generate all d.ts files... (Some may have been generated.)")
            else:
                print("Successfully generated d.ts files!")
        else:
            print("\nSkipping d.ts generation...")
        
        print("\nDone!")
    
    def process_tastypie_schema(self, resource, schema):
        title = to_schema_name(resource)
        schema_fields = schema['fields']
        field_descriptions = self.get_field_descriptions(resource)
        fields = OrderedDict()
        
        valid_prop_converters = {
            'type': 'type',
            'default': 'default',
            'help_text': 'description'
        }
        
        type_key = valid_prop_converters['type']
        description_key = valid_prop_converters['help_text']
        valid_props = [*valid_prop_converters.keys()]
        valid_props.remove('default')
        
        is_valid_prop = lambda x: x in valid_props
        is_default_and_provided = lambda p, v: p == 'default' and not isinstance(v, NOT_PROVIDED)
        
        revisit = []
        required = ["id"]
        for var, spec in schema_fields.items():     # Each field has a specification providing additional details in a tastypie schema
            descriptor = field_descriptions.get(var)
            p = fields[var] = {}
            for prop, value in spec.items():        # For each property and value of the specification
                mapped_prop = valid_prop_converters.get(prop, prop)
                
                if prop == 'help_text':
                    p[mapped_prop] = field_descriptions[var] if var in field_descriptions else ''
                elif is_valid_prop(prop) or is_default_and_provided(prop, value):
                    if isinstance(value, (list, set)):
                        # We treat common collections differently since the only equivalent representation ins TypeScript
                        # is an array.
                        #
                        # Since the type of the array is unknown, we will attempt to determine it's type form the field
                        # type, but this will likely have to be corrected anyway.
                        p['items'] = {
                            **dict([(type_key, 'any')])
                        }
                        revisit.append(var)
                    else:
                        p[mapped_prop] = value
                
                # Sort of unnecessary but helps clientside to know when data is guaranteed.
                if prop == 'nullable' and value:
                    required.append(var)
                
            if descriptor is not None:
                if descriptor.type_override != NO_TYPE:
                    p[type_key] = descriptor.type_override
                p[description_key] = descriptor.description
            
            if p[type_key] == 'float':
                p[type_key] = 'number'
            
        # Revisit array properties to properly set item and array types
        for var in revisit:
            p = fields[var]
            
            if var not in field_descriptions:
                print("WARNING:\tArray type created for '%s.%s', assuming type from schema: '%s'." % (title, var, p[type_key]))
            
            if p[description_key] == '':
                p[description_key] = "Equivalent of TypeScript Array types. A collection of homogeneous or heterogeneous data."
                
            p['items'][type_key] = p[type_key]
            p[type_key] = 'array'
        
        return OrderedDict([
            ('_comments', OUTPUT_COMMENT),
            ('title', title),
            ('type', 'object'),
            ('properties', fields),
            ('required', required)
        ])
    
    def get_field_descriptions(self, resource) -> Dict[str, FieldDescriptor]:
        docstring = resource._meta.model_type.__doc__
        vardocs = {}
        
        if docstring is not None:
            for match in re.finditer(RE_ATTRIBUTE_DEF, docstring):      # Find all attribute docs that can be parsed
                varname = match.group(1).strip()
                type_override = match.group(2)
                vardoc = normalize_whitespace(match.group(3))
                
                field_desc = FieldDescriptor(vardoc)                    # Getting at least a documentation string is guaranteed
                
                """
                    If a type override is specified (not none), first match against the Array Type Override regexp, if
                    no matches are found, attempt to match against the Plain Type Override, if that also fails we attempt
                    the dictionary access anyway. If no match was found, the type_override is set to 'any' (since it is
                    assumed SOME change as desired because the schema is incorrectly identifying type).
                    
                    A warning message is emitted to make the user aware of potentially unwanted behavior.
                """
                if type_override is not None:
                    matches = [*RE_ARRAY_TYPE_OVERRIDE.finditer(type_override)]
                    if len(matches) > 0:
                        field_desc.is_array = True
                        arr_type = matches[0].group(1)
                        type_override = matches[0].group(2)
                    else:
                        matches = [*RE_TYPE_OVERRIDE.finditer(type_override)]
                        if len(matches) > 0:
                            type_override = matches[0].group(1)
                    
                    field_desc.type_override = TYPE_OVERRIDES.get(type_override, DEFAULT_TYPE_OVERRIDE)
                    if field_desc.type_override in [DEFAULT_TYPE_OVERRIDE, NO_TYPE]:
                        overrides = [*TYPE_OVERRIDES.keys()]
                        if field_desc.is_array and arr_type:
                            type_override = '%s[%s]' % (arr_type, type_override)
                            overrides = ['%s[%s]' % (arr_type, o) for o in overrides]
                        print("WARNING:\tDocstring with type override found for %s, but the type is not a valid type "
                              "override (Was given '%s' but must be one of %s). Assuming type override of '%s'." % (varname, type_override, overrides, DEFAULT_TYPE_OVERRIDE))
                
                vardocs[varname] = field_desc
        return vardocs
        

