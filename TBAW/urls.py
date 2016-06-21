from django.conf.urls import url
from .views import team_view, event_view

urlpatterns = [
    url(r'^t/(?P<team_number>[0-9]+)/$', team_view, name='team_view'),
    url(r'^e/(?P<event_key>\d{4}[a-zA-Z]*)', event_view, name='event_view'),
]
