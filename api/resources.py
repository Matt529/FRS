from typing import Type
from django.conf.urls import url

from tastypie.resources import ModelResource, Resource
from tastypie.utils import trailing_slash
from haystack.query import SearchQuerySet

import logging

from FRS.config.tba import urls as tba_urls
from FRS.config.api import names as resnames
from TBAW.models import Team, Event
from util.viewutils import ajax_success
from util.strutils import fqn, varnames_from_fmt

logger = logging.getLogger("django")

class ViewableResource(object):
    def __new__(cls: Type[Resource], *args, **kwargs):
        if not hasattr(cls.Meta, 'frs_url'):
            raise AttributeError("%s is a subclass of %s and must have frs_url* in _meta object." % (fqn(cls), fqn(ViewableResource)))
        
        setattr(cls.Meta, 'frs_url_varnames', varnames_from_fmt(getattr(cls.Meta, 'frs_url')))
        
        return super().__new__(cls, *args)
    
    @classmethod
    def __get_varnames(cls):
        return cls.Meta.frs_url_varnames

    def dehydrate(self: Resource, bundle):
        keyargs = {}
        varnames = self.__get_varnames()
        
        for varname in varnames:
            if varname not in bundle.data:
                raise KeyError("'%s' is a required varname for the frs_url (%s) of %s, but is not available in the data bundle! Is the field available?" % (varname, self._meta.frs_url, fqn(self)))
            keyargs[varname] = bundle.data[varname]
        
        bundle.data['frs_url'] = self._meta.frs_url.format(**keyargs)
        return bundle

class SearchableResource(object):
    
    def __new__(cls: Type[Resource], *args, **kwargs):
        if not hasattr(cls.Meta, 'search_name'):
            logger.warn("WARNING:\t%s is a subclass of %s and does not have a search_name in _meta. One will be generated." % (fqn(cls), fqn(SearchableResource)))
        
        return super().__new__(cls, *args)
    
    @staticmethod
    def __attempt_attr_get(fn, default=None):
        try:
            return fn()
        except AttributeError:
            return default
    
    @staticmethod
    def get_search_urlname(res: Resource):
        return SearchableResource.__attempt_attr_get(lambda: res._meta.search_name, '{}-search'.format(res._meta.resource_name))
    
    def prepend_urls(self: Resource):
        search_name = SearchableResource.get_search_urlname(self)
    
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

class TeamResource(SearchableResource, ViewableResource, ModelResource):
    class Meta:
        model_type = Team
        frs_url = tba_urls.TEAMS().template
        
        queryset = Team.objects.all()
        resource_name = resnames.PUBLIC_TEAMS()
        allowed_methods = ['get']

    def add_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<team_number>[0-9]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def transform_search_results(self, results):
        return results.order_by('team_number')
    

class EventResource(SearchableResource, ViewableResource, ModelResource):
    class Meta:
        model_type = Event
        queryset = Event.objects.all()
        frs_url = tba_urls.EVENTS().template
        
        resource_name = resnames.PUBLIC_EVENTS()
        allowed_methods = ['get']
    
