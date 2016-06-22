from TBAW import views
from django.conf.urls import url

urlpatterns = [
    url(r'^t/(?P<team_number>[0-9]+)/$', views.team_view, name="team_view"),
    url(r'^e/(?P<event_key>\d{4}[a-zA-Z]*)', views.event_view, name="event_view"),
]
