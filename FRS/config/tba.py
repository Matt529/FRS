from typing import Dict

from config._cfg import ConfigValue, is_type
from util.strutils import TemplateLike, varnames_from_fmt, TemplateString

class TbawUrlDefinition(object):
    
    def __init__(self, url_template: TemplateLike, regex_dict: Dict[str, str]):
        self._django_url = url_template.format(**regex_dict)
        self._url_template = url_template.lstrip('^').rstrip('$')
    
    @property
    def template(self):
        return self._url_template
    
    @property
    def urlpattern(self):
        return self._django_url
    
    @staticmethod
    def check_validity(definition: 'TbawUrlDefinition'):
        return len(varnames_from_fmt(definition.urlpattern)) == 0
    
    @staticmethod
    def ensure_validity(definition: 'TbawUrlDefinition'):
        if not TbawUrlDefinition.check_validity(definition):
            raise AssertionError('TBAW URL Definition is invalid, urlpattern as not fully built: "%s" still needs %s' % (definition.urlpattern, varnames_from_fmt(definition._url_template)))
    
    def __str__(self):
        return 'TbawUrl[fmt={}, pattern={}]'.format(self._url_template, self._django_url)

APP_ID = ConfigValue('frs:frs:1', condition=is_type(str))           # type: ConfigValue[str]

class urls:
    TEAMS = ConfigValue(TbawUrlDefinition('^t/{team_number}/$', {'team_number': r'(?P<team_number>\d+)'}), condition=is_type(TbawUrlDefinition))     # type: ConfigValue[TbawUrlDefinition]
    EVENTS = ConfigValue(TbawUrlDefinition('^e/{key}/$', {'key': r'(?P<event_key>\d{4}[a-zA-Z\d]*)'}), condition=is_type(TbawUrlDefinition))         # type: ConfigValue[TbawUrlDefinition]
