from abc import ABCMeta, abstractmethod
from django.db import models
from polymorphic.models import PolymorphicModel


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
                self.wins = int(data_field[7][0])
                self.losses = int(data_field[7][2])
                self.ties = int(data_field[7][4])
                self.played = int(data_field[8])

                print(
                    'rank={0}, rp={1}, auto={2}, scp={3}, goals={4}, def={5}, rec={6}-{7}-{8}, #={9}'.format(
                        self.rank, self.ranking_score, self.auton_points, self.scale_challenge_points,
                        self.goals_points, self.defense_points, self.wins, self.losses, self.ties, self.played))


class RankingModel2015(RankingModel):
    qual_average = models.FloatField(null=True)
    auton_points = models.PositiveSmallIntegerField(null=True)
    container_points = models.PositiveSmallIntegerField(null=True)
    coopertition_points = models.PositiveSmallIntegerField(null=True)
    litter_points = models.PositiveSmallIntegerField(null=True)
    tote_points = models.PositiveSmallIntegerField(null=True)

    def setup(self, rankings_json):
        pass
