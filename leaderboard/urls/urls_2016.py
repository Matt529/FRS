from django.conf.urls import url
from leaderboard.views import Views2016 as views

urls_2016 = [
    url(r'^leaderboard/2016/auton/overall/$', views.highest_team_auton_points, name='highest_team_auton_points'),
    url(r'^leaderboard/2016/auton/average/$', views.highest_team_auton_points_per_game,
        name='highest_team_auton_points_per_game'),
    url(r'^leaderboard/2016/ranking/overall/$', views.highest_team_ranking_points, name='highest_team_ranking_points'),
    url(r'^leaderboard/2016/ranking/average/$', views.highest_team_ranking_points_per_game,
        name='highest_team_ranking_points_per_game'),
    url(r'^leaderboard/2016/scale/overall/$', views.highest_team_scale_challenge_points,
        name='highest_team_scale_points'),
    url(r'^leaderboard/2016/scale/average/$', views.highest_team_scale_challenge_points_per_game,
        name='highest_team_scale_points_per_game'),
    url(r'^leaderboard/2016/goals/overall/$', views.highest_team_goals_points, name='highest_team_goals_points'),
    url(r'^leaderboard/2016/goals/average/$', views.highest_team_goals_points_per_game,
        name='highest_team_goals_points_per_game'),
    url(r'^leaderboard/2016/defense/overall/$', views.highest_team_defense_points, name='highest_team_defense_points'),
    url(r'^leaderboard/2016/defense/average/$', views.highest_team_defense_points_per_game,
        name='highest_team_defense_points_per_game'),
    url(r'^leaderboard/2016/opr/$', views.highest_team_opr, name='highest_team_opr'),
    url(r'^leaderboard/2016/dpr/$', views.highest_team_dpr, name='highest_team_dpr'),
    url(r'^leaderboard/2016/ccwms/$', views.highest_team_ccwms, name='highest_team_ccwms'),
]
