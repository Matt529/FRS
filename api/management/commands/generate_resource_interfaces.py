from django.core.management.base import BaseCommand

from FRS.config._cfg import ConfigValue
from FRS.config.api import names as resnames

from funcy.funcs import map, partial, rpartial
from funcy.types import isa
from funcy.colls import select

from util.strutils import fqn

import api

META_IDENTIFIER_NAME = 'generate_clientside_interface'

def resource_transformer(api_obj):
    return partial(map, api_obj.canonical_resource_for)

to_cv_values = partial(map, lambda cv: cv.value)
select_config = partial(select, isa(ConfigValue))
is_class = isa(type)

get_correct_meta = lambda o: o.Meta if is_class(o) else o._meta
is_marked = lambda o: (lambda x: hasattr(x, META_IDENTIFIER_NAME) and getattr(x, META_IDENTIFIER_NAME))(get_correct_meta(o))
select_with_identifier = partial(select, is_marked)

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('api_name', metavar="API_VERSION", type=str, help="The Name of the API Version (e.g. v1)")
    
    def handle(self, *args, **options):
        api_name = options.pop('api_name')

        frsapi = api.FRSApi.get_instance(api_name)
        possible_resources = resource_transformer(frsapi)(to_cv_values(select_config([*resnames.__dict__.values()])))
        resources = select_with_identifier(possible_resources)

        difference = select(lambda x: x not in resources, possible_resources)
        if len(difference) > 0:
            print("Skipping %s since the %s meta flag is either missing or false." % (map(fqn, difference), META_IDENTIFIER_NAME))
        
        print("Performing Interface Generation for %s" % (', '.join(map(fqn, resources))))
        
        
