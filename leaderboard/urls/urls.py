from django.conf.urls import url

from leaderboard import views

teams = [
    url(r'^leaderboard/teams/elo/$', views.team_elo, name='team_elo'),
    url(r'^leaderboard/teams/matches/$', views.team_match_wins, name='team_matches'),
    url(r'^leaderboard/teams/events/$', views.team_event_wins, name='team_events'),
    url(r'^leaderboard/teams/winrate/$', views.team_win_rate, name='team_winrate'),
    url(r'^leaderboard/teams/awards/$', views.team_award_wins, name='team_awards'),
    url(r'^leaderboard/teams/banners/$', views.team_blue_banners, name='team_blue_banners'),
    url(r'^leaderboard/teams/winstreak/$', views.team_longest_recorded_winstreak, name='team_longest_winstreak'),
    url(r'^leaderboard/teams/winstreak/active/$', views.team_longest_active_winstreak, name='team_active_winstreak'),
]

alliances = [
    url(r'^leaderboard/alliances/events3/$', views.alliance_event_wins_3, name='alliance_events_3'),
    # url(r'^leaderboard/alliances/events2/$', views.alliance_event_wins_2, name='alliance_events_2'),
    url(r'^leaderboard/alliances/matches3/$', views.alliance_match_wins_3, name='alliance_matches_3'),
    url(r'^leaderboard/alliances/elo/$', views.alliance_elo, name='alliance_elo'),
]
