from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from FRS import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('TBAW.urls')),
    url(r'^', include('leaderboard.urls')),
    url(r'^', include('api.urls')),
    url(r'^$', views.landing, name="landing"),
    url(r'^s/', views.search, name="search"),
    url(r'^s2/', views.search_api, name='search_api'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    url(r'^plate/', include('django_spaghetti.urls')),
]
