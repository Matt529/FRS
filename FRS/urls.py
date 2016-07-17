from FRS import views
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('TBAW.urls')),
    url(r'^', include('leaderboard.urls')),
    url(r'^', include('api.urls')),
    url(r'^$', views.landing, name="landing"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    url(r'^plate/', include('django_spaghetti.urls')),
]
