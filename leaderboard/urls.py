from django.conf.urls import url
from leaderboard import views

urlpatterns = [
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^leaderboard/teams/elo/$', views.team_elo, name='team_elo'),
    url(r'^leaderboard/teams/matches/$', views.team_match_wins, name='team_matches'),
    url(r'^leaderboard/teams/events/$', views.team_event_wins, name='team_events'),
    url(r'^leaderboard/teams/winrate/$', views.team_win_rate, name='team_winrate'),
]
