from django.conf.urls import url
from leaderboard import views
from .urls import teams, alliances
from .urls_2016 import urls_2016

urlpatterns = [url(r'^leaderboard/$', views.leaderboard, name='leaderboard')] + teams + alliances + urls_2016
