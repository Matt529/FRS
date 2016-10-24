from django.core.urlresolvers import reverse
from django.shortcuts import render
from leaderboard.models import Leaderboard2016
from util.getters import make_team_table_row, reverse_model_url

DEFAULT_SHOW = 100


class Views2016:
    @staticmethod
    def overview(request):
        high_auton = Leaderboard2016.highest_team_auton_points(1).first()
        high_auton_ppg = Leaderboard2016.highest_team_auton_points_per_game(1).first()
        high_rank = Leaderboard2016.highest_team_ranking_points(1).first()
        high_rank_ppg = Leaderboard2016.highest_team_ranking_points_per_game(1).first()
        high_scale = Leaderboard2016.highest_team_scale_challenge_points(1).first()
        high_scale_ppg = Leaderboard2016.highest_team_scale_challenge_points_per_game(1).first()
        high_goals = Leaderboard2016.highest_team_goals_points(1).first()
        high_goals_ppg = Leaderboard2016.highest_team_goals_points_per_game(1).first()
        high_defense = Leaderboard2016.highest_team_defense_points(1).first()
        high_defense_ppg = Leaderboard2016.highest_team_defense_points_per_game(1).first()
        high_opr = Leaderboard2016.highest_team_opr(1).first()
        high_dpr = Leaderboard2016.highest_team_dpr(1).first()
        high_ccwms = Leaderboard2016.highest_team_ccwms(1).first()

        top = [
            make_team_table_row('Highest Autonomous (Overall)', reverse('highest_team_auton_points'), high_auton.team,
                                high_auton.auton_points),
            make_team_table_row('Highest Autonomous (Per Game)', reverse('highest_team_auton_points_per_game'),
                                high_auton_ppg.team, high_auton_ppg.avg_auton),
            make_team_table_row('Highest Ranking Points (Overall)', reverse('highest_team_ranking_points'), high_rank.team,
                                high_rank.ranking_score),
            make_team_table_row('Highest Ranking Points (Per Game)', reverse('highest_team_ranking_points_per_game'),
                                high_rank_ppg.team, high_rank_ppg.avg_ranking),
            make_team_table_row('Highest Scale/Challenge Points (Overall)', reverse('highest_team_scale_points'),
                                high_scale.team, high_scale.scale_challenge_points),
            make_team_table_row('Highest Scale/Challenge Points (Per Game)', reverse('highest_team_scale_points_per_game'),
                                high_scale_ppg.team, high_scale_ppg.avg_scale),
            make_team_table_row('Highest Goals Points (Overall)', reverse('highest_team_goals_points'), high_goals.team,
                                high_goals.goals_points),
            make_team_table_row('Highest Goals Points (Per Game)', reverse('highest_team_goals_points_per_game'),
                                high_goals_ppg.team, high_goals_ppg.avg_goals),
            make_team_table_row('Highest Defense Points (Overall)', reverse('highest_team_defense_points'), high_defense.team,
                                high_defense.defense_points),
            make_team_table_row('Highest Defense Points (Per Game)', reverse('highest_team_defense_points_per_game'),
                                high_defense_ppg.team, high_defense_ppg.avg_defense),
            make_team_table_row('Highest OPR', reverse('highest_team_opr'), high_opr.team, high_opr.tba_opr),
            make_team_table_row('Highest DPR', reverse('highest_team_dpr'), high_dpr.team, high_dpr.tba_dpr),
            make_team_table_row('Highest CCWMS', reverse('highest_team_ccwms'), high_ccwms.team, high_ccwms.tba_ccwms),
        ]

        return render(request, 'leaderboard/leaderboard.html', context={
            'leaderboard': top
        })

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
            'value': getattr(query_obj, attr, 0),
            'event': query_obj.event.name,
            'event_url': reverse_model_url(query_obj.event)
        }]

    return render(request, 'leaderboard/years/general_table.html', context={'name': name, 'data': data})
