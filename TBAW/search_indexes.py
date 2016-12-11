from haystack import indexes

from TBAW.models import Team, Event

class TeamIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    team_number = indexes.IntegerField(model_attr='team_number')
    name = indexes.CharField(model_attr='name', indexed=True, stored=True, null=True)
    nickname = indexes.CharField(model_attr='nickname', indexed=True, stored=True, null=True)
    key = indexes.CharField(model_attr='key', indexed=True, stored=True)

    def get_model(self):
        return Team


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    key = indexes.CharField(model_attr='key', indexed=True, stored=True)
    name = indexes.CharField(model_attr='name', indexed=True, stored=True)
    nickname = indexes.CharField(model_attr='short_name', indexed=True, stored=True)

    def get_model(self):
        return Event
    
    

