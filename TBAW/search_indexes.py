import re
from haystack import indexes

from TBAW.models import Team, Event

class TeamIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    team_number = indexes.IntegerField(model_attr='team_number', indexed=True, stored=True)
    name = indexes.CharField(model_attr='name', indexed=True, stored=True, null=True, boost=1.05)
    nickname = indexes.CharField(model_attr='nickname', indexed=True, stored=True, null=True, boost=1.01)
    key = indexes.CharField(model_attr='key', indexed=True, stored=True)

    def get_model(self):
        return Team
    
    def prepare_nickname(self, obj: Team):
        if obj.nickname is None:
            return obj.nickname
        
        return obj.nickname.lower()
    
    def prepare_name(self, obj: Team):
        if obj.name is None:
            return obj.name
        
        return obj.name.lower()


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    key = indexes.CharField(model_attr='key', indexed=True, stored=True)
    name = indexes.CharField(model_attr='name', indexed=True, stored=True, boost=1.5)
    nickname = indexes.CharField(model_attr='short_name', indexed=True, stored=True)
    key_name = indexes.CharField(indexed=True, boost=1.25)
    name_parts = indexes.MultiValueField(indexed=True, boost=1.25)

    def get_model(self):
        return Event
    
    def prepare_key_name(self, obj: Event):
        return obj.key[4:]
    
    def prepare_name_parts(self, obj: Event):
        return [obj.name, *re.split(r'\s+', obj.name)]
    

