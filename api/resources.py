from django.conf.urls import url
from tastypie.resources import ModelResource

from TBAW.models import Team, Event


class TeamResource(ModelResource):
    class Meta:
        queryset = Team.objects.all()
        resource_name = 'team'
        allowed_methods = ['get']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<team_number>[0-9]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        allowed_methods = ['get']

