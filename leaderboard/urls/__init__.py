from .urls import teams, alliances
from .urls_2016 import *
from leaderboard import views

urlpatterns = [url(r'^leaderboard/$', views.leaderboard, name='deprecated_leaderboard')] + teams + alliances + urls_2016
