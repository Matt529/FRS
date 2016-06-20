"""FRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from FRS import views
from TBAW import views as tbaw_views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from leaderboard import views as leaderboard_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^t/(?P<team_number>[0-9]+)/$', tbaw_views.team_view, name='team_view'),
    url(r'^leaderboard/$', leaderboard_views.leaderboard, name='leaderboard'),
    url(r'^e/(?P<event_key>\d{4}[a-zA-Z]*)', tbaw_views.event_view, name='event_view'),
    url(r'^$', views.landing, name='landing')
]

urlpatterns += staticfiles_urlpatterns()
