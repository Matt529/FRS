from TBAW.models.scoring.ScoringModel2015 import ScoringModel2015
from TBAW.models.scoring.ScoringModel2016 import ScoringModel2016
from abc import ABCMeta, abstractmethod
from django.db import models
from polymorphic.models import PolymorphicModel


class ScoringModel(PolymorphicModel):
    __metaclass__ = ABCMeta

    red_total_score = models.SmallIntegerField(null=True)
    red_auton_score = models.SmallIntegerField(null=True)
    red_teleop_score = models.SmallIntegerField(null=True)
    red_foul_score = models.SmallIntegerField(null=True)
    red_foul_count = models.SmallIntegerField(default=0, null=True)
    red_tech_foul_count = models.SmallIntegerField(default=0, null=True)

    blue_total_score = models.SmallIntegerField(null=True)
    blue_auton_score = models.SmallIntegerField(null=True)
    blue_teleop_score = models.SmallIntegerField(null=True)
    blue_foul_score = models.SmallIntegerField(null=True)
    blue_foul_count = models.SmallIntegerField(default=0, null=True)
    blue_tech_foul_count = models.SmallIntegerField(default=0, null=True)

    def get_higher_score(self):
        return self.red_total_score if self.red_total_score > self.blue_total_score else self.blue_total_score

    @abstractmethod
    def setup(self, json):
        return

    def __str__(self):
        return "blue: {0}, red: {1}".format(self.blue_total_score, self.red_total_score)
