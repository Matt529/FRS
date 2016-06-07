from TBAW.ranking_models import RankingModel2016
from collections import Counter


class Leaderboard2016:
    @staticmethod
    def highest_auton_points(n=None):
        return RankingModel2016.objects.order_by('-auton_points')[:n]

    @staticmethod
    def highest_auton_points_per_game(n=None):
        auto = Counter()
        # shave off some low auton performances for time
        for rm in RankingModel2016.objects.exclude(auton_points=None).filter(auton_points__gt=200):
            auto[(rm.team, rm.event)] = rm.auton_points / rm.played

        return auto.most_common() if n is None else auto.most_common(n)

    @staticmethod
    def highest_ranking_points(n=None):
        return RankingModel2016.objects.order_by('-ranking_score')[:n]

    @staticmethod
    def highest_ranking_points_per_game(n=None):
        rp = Counter()
        # Shave off the bottom tier performances for time
        for rm in RankingModel2016.objects.exclude(ranking_score=None).filter(ranking_score__gt=20):
            rp[(rm.team, rm.event)] = rm.ranking_score / rm.played

        return rp.most_common() if n is None else rp.most_common(n)

    @staticmethod
    def highest_scale_challenge_points(n=None):
        return RankingModel2016.objects.order_by('-scale_challenge_points')[:n]

    @staticmethod
    def highest_scale_challenge_points_per_game(n=None):
        scp = Counter()
        # shave off bottom tier performances to save time
        for rm in RankingModel2016.objects.exclude(scale_challenge_points=None).filter(scale_challenge_points__gt=150):
            scp[(rm.team, rm.event)] = rm.scale_challenge_points / rm.played

        return scp.most_common() if n is None else scp.most_common(n)

    @staticmethod
    def highest_goals_points(n=None):
        return RankingModel2016.objects.order_by('-goals_points')[:n]

    @staticmethod
    def highest_goals_points_per_game(n=None):
        gp = Counter()
        for rm in RankingModel2016.objects.exclude(goals_points=None).filter(goals_points__gt=290):
            gp[(rm.team, rm.event)] = rm.goals_points / rm.played

        return gp.most_common() if n is None else gp.most_common(n)

    @staticmethod
    def highest_defense_points(n=None):
        return RankingModel2016.objects.order_by('-defense_points')[:n]

    @staticmethod
    def highest_defense_points_per_game(n=None):
        df = Counter()
        for rm in RankingModel2016.objects.exclude(defense_points=None).filter(defense_points__gt=550):
            df[(rm.team, rm.event)] = rm.defense_points / rm.played

        return df.most_common() if n is None else df.most_common(n)

    @staticmethod
    def highest_opr(n=None):
        return RankingModel2016.objects.order_by('-tba_opr')[:n]

    @staticmethod
    def highest_dpr(n=None):
        return RankingModel2016.objects.order_by('-tba_dpr')[:n]

    @staticmethod
    def highest_ccwms(n=None):
        return RankingModel2016.objects.order_by('-tba_ccwms')[:n]
