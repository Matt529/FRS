from TBAW.models import RankingModel2016, Event, Match
from collections import Counter
from django.db.models import F, ExpressionWrapper, FloatField, Sum, Count


class Leaderboard2016:
    @staticmethod
    def highest_team_auton_points(n=None):
        return RankingModel2016.objects.order_by('-auton_points')[:n]

    @staticmethod
    def highest_team_auton_points_per_game(n=None):
        return RankingModel2016.objects.annotate(
            avg_auton=ExpressionWrapper(F('auton_points') * 1.0 / F('played'), output_field=FloatField())).order_by(
            '-avg_auton')[:n]

    @staticmethod
    def highest_team_ranking_points(n=None):
        return RankingModel2016.objects.order_by('-ranking_score')[:n]

    @staticmethod
    def highest_team_ranking_points_per_game(n=None):
        return RankingModel2016.objects.annotate(
            avg_ranking=ExpressionWrapper(F('ranking_score') * 1.0 / F('played'), output_field=FloatField())).order_by(
            '-avg_ranking')[:n]

    @staticmethod
    def highest_team_scale_challenge_points(n=None):
        return RankingModel2016.objects.order_by('-scale_challenge_points')[:n]

    @staticmethod
    def highest_team_scale_challenge_points_per_game(n=None):
        return RankingModel2016.objects.annotate(
            avg_scale=ExpressionWrapper(F('scale_challenge_points') * 1.0 / F('played'),
                                        output_field=FloatField())).order_by('-avg_scale')[:n]

    @staticmethod
    def highest_team_goals_points(n=None):
        return RankingModel2016.objects.order_by('-goals_points')[:n]

    @staticmethod
    def highest_team_goals_points_per_game(n=None):
        return RankingModel2016.objects.annotate(
            avg_goals=ExpressionWrapper(F('goals_points') * 1.0 / F('played'),
                                        output_field=FloatField())).order_by('-avg_goals')[:n]

    @staticmethod
    def highest_team_defense_points(n=None):
        return RankingModel2016.objects.order_by('-defense_points')[:n]

    @staticmethod
    def highest_team_defense_points_per_game(n=None):
        return RankingModel2016.objects.annotate(
            avg_defense=ExpressionWrapper(F('defense_points') * 1.0 / F('played'),
                                          output_field=FloatField())).order_by('-avg_defense')[:n]

    @staticmethod
    def highest_team_opr(n=None):
        return RankingModel2016.objects.order_by('-tba_opr')[:n]

    @staticmethod
    def highest_team_dpr(n=None):
        return RankingModel2016.objects.order_by('-tba_dpr')[:n]

    @staticmethod
    def highest_team_ccwms(n=None):
        return RankingModel2016.objects.order_by('-tba_ccwms')[:n]

    @staticmethod
    def highest_event_match_average_score(n=None):
        return Event.objects.annotate(
            sum_blue=ExpressionWrapper(Sum('match__scoring_model__blue_total_score'), output_field=FloatField()),
            sum_red=ExpressionWrapper(Sum('match__scoring_model__red_total_score'), output_field=FloatField()),
            count_blue=ExpressionWrapper(Count('match__scoring_model__blue_total_score'), output_field=FloatField()),
            count_red=ExpressionWrapper(Count('match__scoring_model__red_total_score'), output_field=FloatField())
        ).annotate(
            avg_score=ExpressionWrapper((F('sum_blue') + F('sum_red')) * 1.0 / (F('count_blue') + F('count_red')),
                                        output_field=FloatField())
        ).order_by('-avg_score')[:n]

    @staticmethod
    def highest_region_average_score(n=None):
        # This takes forever, don't use it until we replace it with Django annotations
        matches = Match.objects.filter(event__year=2016)
        totals = Counter()
        counts = Counter()
        for match in matches:
            for alliance in match.alliances.all():
                for team in alliance.teams.all():
                    counts['{0}, {1}'.format(team.region, team.country_name)] += 1
                    if alliance.get_color_display() == 'Red':
                        totals['{0}, {1}'.format(team.region, team.country_name)] += \
                            match.scoring_model.red_total_score
                    else:
                        totals['{0}, {1}'.format(team.region, team.country_name)] += \
                            match.scoring_model.blue_total_score

        for key, value in totals.most_common():
            totals[key] = totals[key] / counts[key]

        return totals.most_common() if n is None else totals.most_common(n)
