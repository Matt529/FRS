from django.conf.urls import url

urlpatterns = [
    url(r'^t/(?P<team_number>[0-9]+)/$', 'TBAW.views.team_view'),
    url(r'^e/(?P<event_key>\d{4}[a-zA-Z]*)', 'TBAW.views.event_view'),
]
