from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dashing.utils import router as dashing_routes

from FRS import views
from api import FRSApi
from api.resources import TeamResource, EventResource

api_v1 = FRSApi(api_name='v1')
api_v1.register(TeamResource())
api_v1.register(EventResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('TBAW.urls')),
    url(r'^', include('leaderboard.urls')),
    url(r'^$', views.landing, name='landing'),
    url(r'^s/', views.search, name='search'),
    url(r'^s2/', views.search_api, name='search_api'),
    url(r'^api/', include(api_v1.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^l/', include('leaderboard2.urls')),
    url(r'^dashboard/', include(dashing_routes.urls)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    url(r'^plate/', include('django_spaghetti.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
