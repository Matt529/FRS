from abc import ABCMeta, abstractmethod

from bulk_update.manager import BulkUpdateManager
from django.db import models
from polymorphic.models import PolymorphicModel

from TBAW.models import Team, Event


class RankingModel(PolymorphicModel):
    __metaclass__ = ABCMeta

    rank = models.PositiveSmallIntegerField(null=True)
    team = models.ForeignKey(Team, null=True)
    played = models.PositiveSmallIntegerField(null=True)
    tba_opr = models.FloatField(null=True)
    tba_dpr = models.FloatField(null=True)
    tba_ccwms = models.FloatField(null=True)
    event = models.ForeignKey(Event, null=True)
    elo_mu_pre = models.FloatField(null=True, default=0)
    elo_mu_post = models.FloatField(null=True, default=0)
    elo_sigma_pre = models.FloatField(null=True, default=0)
    elo_sigma_post = models.FloatField(null=True, default=0)

    qual_wins = models.PositiveSmallIntegerField(default=0)
    qual_losses = models.PositiveSmallIntegerField(default=0)
    qual_ties = models.PositiveSmallIntegerField(default=0)

    total_wins = models.PositiveSmallIntegerField(default=0)
    total_losses = models.PositiveSmallIntegerField(default=0)
    total_ties = models.PositiveSmallIntegerField(default=0)

    objects = BulkUpdateManager()

    @abstractmethod
    def setup(self, rankings_json) -> None:
        pass

    def get_record(self) -> str:
        return "{0}-{1}-{2} ({3}-{4}-{5})".format(self.total_wins, self.total_losses, self.total_ties, self.qual_wins,
                                                  self.qual_losses, self.qual_ties)

    def __repr__(self):
        return "{0}. {1} [{2}-{3}-{4}] ({5})".format(self.rank, self.team, self.total_wins, self.total_losses,
                                                     self.total_ties, self.event)


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
        for data_field in rankings_json[1:]:
            if int(data_field[1]) == self.team.team_number:
                self.rank = int(data_field[0])
                self.qual_average = float(data_field[2])
                self.auton_points = int(data_field[3])
                self.container_points = int(data_field[4])
                self.coopertition_points = int(data_field[5])
                self.litter_points = int(data_field[6])
                self.tote_points = int(data_field[7])
                self.played = int(data_field[8])


class RankingModel2014(RankingModel):
    qual_score = models.PositiveSmallIntegerField(null=True)
    assist_points = models.PositiveSmallIntegerField(null=True)
    truss_catch_points = models.PositiveSmallIntegerField(null=True)
    auton_points = models.PositiveSmallIntegerField(null=True)
    teleop_points = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json):
        for data_field in rankings_json[1:]:
            if int(data_field[1]) == self.team.team_number:
                self.rank = int(data_field[0])
                self.qual_score = int(float(data_field[2]))
                self.assist_points = int(float(data_field[3]))
                self.auton_points = int(float(data_field[4]))
                self.truss_catch_points = int(float(data_field[5]))
                self.teleop_points = int(float(data_field[6]))
                record = [int(s) for s in data_field[7].split('-') if s.isdigit()]
                self.qual_wins = record[0]
                self.qual_losses = record[1]
                self.qual_ties = record[2]
                self.played = int(data_field[8])


class RankingModel2013(RankingModel):
    qual_score = models.PositiveSmallIntegerField(null=True)
    climb_points = models.PositiveSmallIntegerField(null=True)
    auton_points = models.PositiveSmallIntegerField(null=True)
    teleop_points = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json) -> None:
        for data_field in rankings_json[1:]:
            if int(data_field[1]) == self.team.team_number:
                if "HP" in data_field:  # Week 1 events in 2013 seem to have different API returns from TBA
                    record_str = data_field[7]
                    played = data_field[9]
                else:
                    record_str = data_field[6]
                    played = data_field[8]

                self.rank = int(data_field[0])
                self.qual_score = int(float(data_field[2]))
                self.auton_points = int(float(data_field[3]))
                self.climb_points = int(float(data_field[4]))
                self.teleop_points = int(float(data_field[5]))
                record = [int(s) for s in record_str.split('-') if s.isdigit()]
                self.qual_wins = record[0]
                self.qual_losses = record[1]
                self.qual_ties = record[2]
                self.played = int(played)


class RankingModel2012(RankingModel):
    qual_score = models.PositiveSmallIntegerField(null=True)
    auton_points = models.PositiveSmallIntegerField(null=True)
    bridge_points = models.PositiveSmallIntegerField(null=True)
    teleop_points = models.PositiveSmallIntegerField(null=True)
    coopertition_points = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json) -> None:
        for data_field in rankings_json[1:]:
            if int(data_field[1]) == self.team.team_number:
                self.rank = data_field[0]
                self.qual_score = data_field[2]
                self.auton_points = data_field[3]
                self.bridge_points = data_field[4]
                self.teleop_points = data_field[5]
                self.coopertition_points = data_field[6]
                record = [int(s) for s in data_field[7].split('-') if s.isdigit()]
                self.qual_wins = record[0]
                self.qual_losses = record[1]
                self.qual_ties = record[2]
                self.played = int(data_field[8])


class RankingModel2011(RankingModel):
    qual_score = models.PositiveSmallIntegerField(null=True)
    ranking_score = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json) -> None:
        for data_field in rankings_json[1:]:
            if int(data_field[1]) == self.team.team_number:
                self.rank = int(data_field[0])
                self.qual_wins = int(data_field[2])
                self.qual_losses = int(data_field[3])
                self.qual_ties = int(data_field[4])
                self.played = int(data_field[5])
                self.qual_score = int(data_field[6])
                self.ranking_score = int(data_field[7])


class RankingModel2010(RankingModel):
    seeding_score = models.PositiveSmallIntegerField(null=True)
    coopertition_bonus = models.PositiveSmallIntegerField(null=True)
    hanging_points = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json) -> None:
        pass
