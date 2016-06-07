from abc import ABCMeta, abstractmethod
from django.db import models
from polymorphic.models import PolymorphicModel


def parse_record(record_str):
    """Quick little helper function to turn a string record, e.g. 5-4-1, to [5, 4, 1]"""
    return [int(s) for s in record_str.split('-') if s.isdigit()]


class RankingModel(PolymorphicModel):
    __metaclass__ = ABCMeta

    rank = models.PositiveSmallIntegerField(null=True)
    team = models.ForeignKey('TBAW.Team', null=True)
    wins = models.PositiveSmallIntegerField(null=True)
    losses = models.PositiveSmallIntegerField(null=True)
    ties = models.PositiveSmallIntegerField(null=True)
    played = models.PositiveSmallIntegerField(null=True)
    tba_opr = models.FloatField(null=True)
    tba_dpr = models.FloatField(null=True)
    tba_ccwms = models.FloatField(null=True)
    event = models.ForeignKey('TBAW.Event', null=True)

    @abstractmethod
    def setup(self, rankings_json):
        pass


class RankingModel2016(RankingModel):
    ranking_score = models.PositiveSmallIntegerField(null=True)
    auton_points = models.PositiveSmallIntegerField(null=True)
    scale_challenge_points = models.PositiveSmallIntegerField(null=True)
    goals_points = models.PositiveSmallIntegerField(null=True)
    defense_points = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json):
        for data_field in rankings_json[1:]:
            if int(data_field[1]) == self.team.team_number:
                self.rank = int(data_field[0])
                self.ranking_score = int(float(data_field[2]))
                self.auton_points = int(float(data_field[3]))
                self.scale_challenge_points = int(float(data_field[4]))
                self.goals_points = int(float(data_field[5]))
                self.defense_points = int(float(data_field[6]))
                record = parse_record(data_field[7])
                self.wins = record[0]
                self.losses = record[1]
                self.ties = record[2]
                self.played = int(data_field[8])


class RankingModel2015(RankingModel):
    qual_average = models.FloatField(null=True)
    auton_points = models.PositiveSmallIntegerField(null=True)
    container_points = models.PositiveSmallIntegerField(null=True)
    coopertition_points = models.PositiveSmallIntegerField(null=True)
    litter_points = models.PositiveSmallIntegerField(null=True)
    tote_points = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json):
        pass
