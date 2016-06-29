from django.conf.urls import url
from leaderboard.views import Views2016

highest_team_auton_points_str = 'highest_team_auton_points'
highest_team_auton_points_per_game_str = 'highest_team_auton_points_per_game'
highest_team_ranking_points_str = 'highest_team_ranking_points'
highest_team_ranking_points_per_game_str = 'highest_team_ranking_points_per_game'
highest_team_scale_challenge_points_str = 'highest_team_scale_points'
highest_team_scale_challenge_points_per_game_str = 'highest_team_scale_points_per_game'
highest_team_goals_points_str = 'highest_team_goals_points'
highest_team_goals_points_per_game_str = 'highest_team_goals_points_per_game'
highest_team_defense_points_str = 'highest_team_defense_points'
highest_team_defense_points_per_game_str = 'highest_team_defense_points_per_game'
highest_team_opr_str = 'highest_team_opr'
highest_team_dpr_str = 'highest_team_dpr'
highest_team_ccwms_str = 'highest_team_ccwms'

urls_2016 = [
    # todo: make a get_view for a regex with leaderboard/<year>/$
    url(r'^leaderboard/2016/$', Views2016.overview, name='overview'),
    url(r'^leaderboard/2016/auton/overall/$', Views2016.highest_team_auton_points, name=highest_team_auton_points_str),
    url(r'^leaderboard/2016/auton/average/$', Views2016.highest_team_auton_points_per_game,
        name=highest_team_auton_points_per_game_str),
    url(r'^leaderboard/2016/ranking/overall/$', Views2016.highest_team_ranking_points,
        name=highest_team_ranking_points_str),
    url(r'^leaderboard/2016/ranking/average/$', Views2016.highest_team_ranking_points_per_game,
        name=highest_team_ranking_points_per_game_str),
    url(r'^leaderboard/2016/scale/overall/$', Views2016.highest_team_scale_challenge_points,
        name=highest_team_scale_challenge_points_str),
    url(r'^leaderboard/2016/scale/average/$', Views2016.highest_team_scale_challenge_points_per_game,
        name=highest_team_scale_challenge_points_per_game_str),
    url(r'^leaderboard/2016/goals/overall/$', Views2016.highest_team_goals_points, name=highest_team_goals_points_str),
    url(r'^leaderboard/2016/goals/average/$', Views2016.highest_team_goals_points_per_game,
        name=highest_team_goals_points_per_game_str),
    url(r'^leaderboard/2016/defense/overall/$', Views2016.highest_team_defense_points,
        name=highest_team_defense_points_str),
    url(r'^leaderboard/2016/defense/average/$', Views2016.highest_team_defense_points_per_game,
        name=highest_team_defense_points_per_game_str),
    url(r'^leaderboard/2016/opr/$', Views2016.highest_team_opr, name=highest_team_opr_str),
    url(r'^leaderboard/2016/dpr/$', Views2016.highest_team_dpr, name=highest_team_dpr_str),
    url(r'^leaderboard/2016/ccwms/$', Views2016.highest_team_ccwms, name=highest_team_ccwms_str),
]
