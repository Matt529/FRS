from django.conf.urls import url
from leaderboard import views

urlpatterns = [
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^leaderboard/elo/$', views.elo_leaders, name='elo_leaders')
]
