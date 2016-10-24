from TBAW import views
from django.conf.urls import url

urlpatterns = [
    url(r'^t/(?P<team_number>\d+)/$', views.team_view, name="team_view"),
    url(r'^e/(?P<event_key>\d{4}[a-zA-Z\d]*)/$', views.event_view, name="event_view"),
    url(r'^a/(?P<team1>[0-9]+)/(?P<team2>[0-9]+)/(?P<team3>[0-9]+)/', views.alliance_view, name="alliance_view")
]


