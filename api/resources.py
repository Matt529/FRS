from django.conf.urls import url

from tastypie.resources import ModelResource, Resource
from tastypie.utils import trailing_slash
from haystack.query import SearchQuerySet

from TBAW.models import Team, Event
from util.viewutils import ajax_success

class SearchableResource(object):
    
    @staticmethod
    def __attempt_attr_get(fn, default=None):
        try:
            return fn()
        except AttributeError:
            return default
    
    def prepend_urls(self: Resource):
        search_name = SearchableResource.__attempt_attr_get(lambda: self._meta.search_name, '{}-search'.format(self._meta.resource_name))
    
        return [
            url(r"^(?P<resource_name>%s)/search%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('_resource_search'), name=search_name),
            *self.add_urls()
        ]
    
    def _resource_search(self: ModelResource, request, **kwargs):
        mixin_self = self   # type: SearchableResource
        
        self.method_check(request, allowed=['get'])
        # Uncomment when authentication is set up
        # self.is_authenticated(request)
        self.throttle_check(request)
    
        get_params = request.GET
        query = get_params.get('query')     # type: str
        limit = int(get_params.get('limit', 0))  # type: int
        
        results = SearchQuerySet().models(self._meta.model_type).load_all().auto_query(query)
        results = mixin_self.transform_search_results(results)
        
        if limit != 0:
            results = results[:limit]
            
        objects = []
        for result in results:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
            
        self.log_throttled_access(request)
        return self.create_response(request, ajax_success(objects=objects))
    
    def add_urls(self):
        return []
    
    def transform_search_results(self, results: SearchQuerySet):
        return results

class TeamResource(SearchableResource, ModelResource):
    class Meta:
        model_type = Team
        queryset = Team.objects.all()
        resource_name = 'team'
        allowed_methods = ['get']

    def add_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<team_number>[0-9]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def transform_search_results(self, results):
        return results.order_by('team_number')


class EventResource(SearchableResource, ModelResource):
    class Meta:
        model_type = Event
        queryset = Event.objects.all()
        resource_name = 'event'
        allowed_methods = ['get']
    
