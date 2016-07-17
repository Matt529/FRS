from api import views
from django.conf.urls import url

urlpatterns = [
    url(r'^api/team/(?P<team_number>[0-9]+)/$', views.team_json, name='team_json'),
    url(r'^api/teams/(?P<page>\d+)/$', views.team_list_json, name='team_list_json'),
    url(r'^api/event/(?P<event_key>\d{4}[a-zA-Z\d]*)/$', views.event_json, name='event_json'),
    url(r'^api/events/(?P<page>\d+)/$', views.event_list_json, name='event_list_json'),
]
