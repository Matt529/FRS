from TBAW.models import Team, Event
from abc import ABCMeta, abstractmethod
from django.db import models
from polymorphic.models import PolymorphicModel


class RankingModel(PolymorphicModel):
    __metaclass__ = ABCMeta

    rank = models.PositiveSmallIntegerField(null=True)
    team = models.ForeignKey(Team, null=True)
    played = models.PositiveSmallIntegerField(null=True)
    tba_opr = models.FloatField(null=True)
    tba_dpr = models.FloatField(null=True)
    tba_ccwms = models.FloatField(null=True)
    event = models.ForeignKey(Event, null=True)
    elo_mu_pre = models.FloatField(null=True)
    elo_mu_post = models.FloatField(null=True)
    elo_sigma_pre = models.FloatField(null=True)
    elo_sigma_post = models.FloatField(null=True)

    qual_wins = models.PositiveSmallIntegerField(null=True)
    qual_losses = models.PositiveSmallIntegerField(null=True)
    qual_ties = models.PositiveSmallIntegerField(null=True)

    @abstractmethod
    def setup(self, rankings_json):
        pass

    def get_record(self):
        return "{0}-{1}-{2}".format(self.qual_wins, self.qual_losses, self.qual_ties)

    def __repr__(self):
        return "{0}. {1} [{2}-{3}-{4}] ({5})".format(self.rank, self.team, self.wins, self.losses, self.ties,
                                                     self.event)


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
                record = [int(s) for s in data_field[7].split('-') if s.isdigit()]
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
