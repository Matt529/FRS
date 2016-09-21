from abc import ABCMeta, abstractmethod

from django.db import models
from polymorphic.models import PolymorphicModel

from TBAW.models import Team, ScoringModel, RankingModel, Alliance


class Leaderboard(PolymorphicModel):
    __metaclass__ = ABCMeta

    description = models.TextField(default="", null=False)
    field = models.CharField(default="", null=False, max_length=50)

    @abstractmethod
    def get_models(self):
        return

    def get_leaderboard_tuples(self):
        selector = self.field[self.field.startswith('-'):]
        return [(m, getattr(m, selector)) for m in self.get_models().order_by(self.field)]

    def get_leader(self):
        return self.get_models().order_by(self.field).first()


class TeamLeaderboard(Leaderboard):
    teams = models.ManyToManyField(Team)

    def get_models(self):
        return self.teams


class AllianceLeaderboard(Leaderboard):
    alliances = models.ManyToManyField(Alliance)

    def get_models(self):
        return self.alliances


class ScoringLeaderboard(Leaderboard):
    scoring_models = models.ManyToManyField(ScoringModel)

    def get_models(self):
        return self.scoring_models


class RankingLeaderboard(Leaderboard):
    ranking_models = models.ManyToManyField(RankingModel)

    def get_models(self):
        return self.ranking_models
