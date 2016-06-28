from TBAW import views, models
from django.conf.urls import url
from django.core.urlresolvers import reverse

urlpatterns = [
    url(r'^t/(?P<team_number>[0-9]+)/$', views.team_view, name="team_view"),
    url(r'^e/(?P<event_key>\d{4}[a-zA-Z\d]*)/$', views.event_view, name="event_view"),
    url(r'^a/(?P<team1>[0-9]+)/(?P<team2>[0-9]+)/(?P<team3>[0-9]+)/', views.alliance_view, name="alliance_view")
]


def reverse_model_url(model):
    data = None

    if type(model) is models.Team:
        data = reverse('team_view', kwargs={'team_number': model.team_number})
    elif type(model) is models.Event:
        data = reverse('event_view', kwargs={'event_key': model.key})
    elif type(model) is models.Alliance:
        data = reverse('alliance_view', kwargs={
            'team1': model.teams.all()[0].team_number,
            'team2': model.teams.all()[1].team_number,
            'team3': model.teams.all()[2].team_number
        })
    else:
        raise Exception('Cannot find a url for that model!')

    return data
