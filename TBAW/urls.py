from TBAW import views
from django.conf.urls import url

from FRS.config.tba import urls as tba_urls

urlpatterns = [
    url(tba_urls.TEAMS().urlpattern, views.team_view, name="team_view"),
    url(tba_urls.EVENTS().urlpattern, views.event_view, name="event_view"),
    url(r'^a/(?P<team1>[0-9]+)/(?P<team2>[0-9]+)/(?P<team3>[0-9]+)/', views.alliance_view, name="alliance_view")
]


