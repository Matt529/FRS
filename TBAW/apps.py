from django.apps import AppConfig
from watson import search as watson

class TbawConfig(AppConfig):
    name = 'TBAW'
    def ready(self):
        for model in [self.get_model('Team'), self.get_model('Event')]:
            watson.register(model)
