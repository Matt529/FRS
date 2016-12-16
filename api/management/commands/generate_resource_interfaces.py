from django.core.management.base import BaseCommand

from FRS.config._cfg import ConfigValue
from FRS.config.api import names as resnames

from funcy.funcs import map, partial
from funcy.types import isa
from funcy.colls import select

from util.strutils import fqn

import api

to_cv_values = partial(map, lambda cv: cv.value)
select_config = partial(select, isa(ConfigValue))

def resource_transformer(api_obj):
    return partial(map, api_obj.canonical_resource_for)

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('api_name', metavar="API_VERSION", type=str, help="The Name of the API Version (e.g. v1)")
    
    def handle(self, *args, **options):
        api_name = options.pop('api_name')

        frsapi = api.FRSApi.get_instance(api_name)
        resources = resource_transformer(frsapi)(to_cv_values(select_config([*resnames.__dict__.values()])))
        resource_fqns = map(fqn, resources)
        
        print("Performing Interface Generation for %s" % (', '.join(resource_fqns)))
        
        
