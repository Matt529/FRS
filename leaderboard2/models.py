from abc import ABCMeta, abstractmethod

from django.db import models
from django.db.models import F
from polymorphic.models import PolymorphicModel

from TBAW.models import Team, ScoringModel2016, RankingModel, Alliance


class Leaderboard(PolymorphicModel):
    __metaclass__ = ABCMeta

    selector = models.CharField(default='-ret_field', null=True, max_length=50)
    description = models.TextField(default="", null=False)
    field_1 = models.CharField(null=True, max_length=50)
    field_2 = models.CharField(null=True, max_length=50)
    field_3 = models.CharField(null=True, max_length=50)

    def __get_fields(self):
        fields = []
        extras = [self.field_2, self.field_3]
        for ex in extras:
            if ex is not None:
                fields.append(ex[ex.startswith('-'):])

        return fields

    @abstractmethod
    def get_models(self):
        return

    def annotate_queryset(self, queryset):
        queryset = queryset.annotate(ret_field=F(self.field_1[self.field_1.startswith('-'):]))
        for extra_field in self.__get_fields():
            queryset = queryset.annotate(ret_field=F('ret_field') + F(extra_field))

        return queryset

    def get_detailed_models(self, qs):
        return self.annotate_queryset(qs)

    def get_selector(self):
        return self.selector[self.selector.startswith('-'):]

    def get_order_by(self):
        return self.selector

    def get_leaderboard_tuples(self):
        return [(m, getattr(m, self.get_selector())) for m in self.get_models().order_by(self.get_order_by())]

    def get_leaders(self):
        leaders = self.get_models().order_by(self.get_order_by())
        top_value = getattr(leaders.first(), self.get_selector())
        top_leaders = [t for t in leaders if getattr(t, self.get_selector()) == top_value]

        return top_leaders

    def get_leading_value(self):
        return getattr(self.get_models().order_by(self.get_order_by()).first(), self.get_selector())


class TeamLeaderboard(Leaderboard):
    teams = models.ManyToManyField(Team)

    def get_models(self):
        return self.get_detailed_models(self.teams.all())


class AllianceLeaderboard(Leaderboard):
    alliances = models.ManyToManyField(Alliance)

    def get_models(self):
        return self.alliances


class ScoringLeaderboard2016(Leaderboard):
    scoring_models = models.ManyToManyField(ScoringModel2016)

    def get_models(self):
        return self.get_detailed_models(self.scoring_models.all())


class RankingLeaderboard(Leaderboard):
    ranking_models = models.ManyToManyField(RankingModel)

    def get_models(self):
        return self.ranking_models
