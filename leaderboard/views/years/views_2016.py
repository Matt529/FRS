from TBAW.urls import reverse_model_url
from django.shortcuts import render
from leaderboard.models import Leaderboard2016

DEFAULT_SHOW = 100


class Views2016:
    @staticmethod
    def highest_team_auton_points(request):
        return make_table_page(request, 'Highest Auton Points (Overall)',
                               Leaderboard2016.highest_team_auton_points(DEFAULT_SHOW),
                               'auton_points')

    @staticmethod
    def highest_team_auton_points_per_game(request):
        return make_table_page(request, 'Highest Auton Points (Per Game)',
                               Leaderboard2016.highest_team_auton_points_per_game(DEFAULT_SHOW),
                               'avg_auton')

    @staticmethod
    def highest_team_ranking_points(request):
        return make_table_page(request, 'Highest Ranking Points (Overall)',
                               Leaderboard2016.highest_team_ranking_points(DEFAULT_SHOW),
                               'ranking_score')

    @staticmethod
    def highest_team_ranking_points_per_game(request):
        return make_table_page(request, 'Highest Ranking Points (Per Game)',
                               Leaderboard2016.highest_team_ranking_points_per_game(DEFAULT_SHOW),
                               'avg_ranking')

    @staticmethod
    def highest_team_scale_challenge_points(request):
        return make_table_page(request, 'Highest Scale/Challenge Points (Overall)',
                               Leaderboard2016.highest_team_scale_challenge_points(DEFAULT_SHOW),
                               'scale_challenge_points')

    @staticmethod
    def highest_team_scale_challenge_points_per_game(request):
        return make_table_page(request, 'Highest Scale/Challenge Points (Per Game)',
                               Leaderboard2016.highest_team_scale_challenge_points_per_game(DEFAULT_SHOW),
                               'avg_scale')

    @staticmethod
    def highest_team_goals_points(request):
        return make_table_page(request, 'Highest Goals Points (Overall)',
                               Leaderboard2016.highest_team_goals_points(DEFAULT_SHOW),
                               'goals_points')

    @staticmethod
    def highest_team_goals_points_per_game(request):
        return make_table_page(request, 'Highest Goals Points (Per Game)',
                               Leaderboard2016.highest_team_goals_points_per_game(DEFAULT_SHOW),
                               'avg_goals')

    @staticmethod
    def highest_team_defense_points(request):
        return make_table_page(request, 'Highest Defense Points (Overall)',
                               Leaderboard2016.highest_team_defense_points(DEFAULT_SHOW),
                               'defense_points')

    @staticmethod
    def highest_team_defense_points_per_game(request):
        return make_table_page(request, 'Highest Defense Points (Per Game)',
                               Leaderboard2016.highest_team_defense_points_per_game(DEFAULT_SHOW),
                               'avg_defense')

    @staticmethod
    def highest_team_opr(request):
        return make_table_page(request, 'Highest OPR', Leaderboard2016.highest_team_opr(DEFAULT_SHOW), 'tba_opr')

    @staticmethod
    def highest_team_dpr(request):
        return make_table_page(request, 'Highest DPR', Leaderboard2016.highest_team_dpr(DEFAULT_SHOW), 'tba_dpr')

    @staticmethod
    def highest_team_ccwms(request):
        return make_table_page(request, 'Highest CCWMS', Leaderboard2016.highest_team_ccwms(DEFAULT_SHOW), 'tba_ccwms')

        # @staticmethod
        # def highest_event_match_average_score(request):
        #     return render(request, '', context={
        #         'avg_score': Leaderboard2016.highest_event_match_average_score(DEFAULT_SHOW)
        #     })
        #
        #
        # @staticmethod
        # def highest_score_matches(request):
        #     return render(request, '', context={
        #         'high_score': Leaderboard2016.highest_score_matches(DEFAULT_SHOW)
        #     })


def make_table_page(request, name, query_set, attr):
    data = []
    for query_obj in query_set:
        data += [{
            'holder': query_obj.team,
            'holder_url': reverse_model_url(query_obj.team),
            'value': getattr(query_obj, attr, 0)
        }]

    return render(request, 'leaderboard/years/general_table.html', context={'name': name, 'data': data})
