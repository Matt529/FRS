from json import loads, dumps

from abc import ABCMeta, abstractmethod
from django.db import models
from polymorphic.models import PolymorphicModel


class ScoringModel(PolymorphicModel):
    __metaclass__ = ABCMeta

    json_data = models.TextField(default='', null=True)

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

    def get_json_data(self):
        return loads(self.json_data)

    def set_json_data(self, data):
        self.json_data = dumps(data)

    @abstractmethod
    def setup(self, json):
        return


class ScoringModel2016(ScoringModel):
    # constant point values
    POINTS_AUTON_REACH_DEFENSE = 2
    POINTS_AUTON_CROSS_DEFENSE = 10
    POINTS_AUTON_BOULDER_LOW = 5
    POINTS_AUTON_BOULDER_HIGH = 10
    POINTS_TELEOP_BOULDER_LOW = 2
    POINTS_TELEOP_BOULDER_HIGH = 5

    blue_adjust_points = models.SmallIntegerField(default=0, null=True)
    blue_auton_boulders_high = models.SmallIntegerField(default=0, null=True)
    blue_auton_boulders_low = models.SmallIntegerField(default=0, null=True)
    blue_auton_boulders_points = models.SmallIntegerField(default=0, null=True)
    blue_auton_crossing_points = models.SmallIntegerField(default=0, null=True)
    blue_auton_reach_points = models.SmallIntegerField(default=0, null=True)
    blue_breach_points = models.SmallIntegerField(default=0, null=True)
    blue_capture_points = models.SmallIntegerField(default=0, null=True)
    blue_defense1 = models.CharField(max_length=20, default='', null=True)
    blue_defense2 = models.CharField(max_length=20, default='', null=True)
    blue_defense3 = models.CharField(max_length=20, default='', null=True)
    blue_defense4 = models.CharField(max_length=20, default='', null=True)
    blue_defense1_cross_count = models.SmallIntegerField(default=0, null=True)
    blue_defense2_cross_count = models.SmallIntegerField(default=0, null=True)
    blue_defense3_cross_count = models.SmallIntegerField(default=0, null=True)
    blue_defense4_cross_count = models.SmallIntegerField(default=0, null=True)
    blue_defenses_breached = models.NullBooleanField(default=False)
    blue_low_bar_cross_count = models.SmallIntegerField(default=0, null=True)
    blue_robot1_auto = models.CharField(max_length=20, default='', null=True)
    blue_robot2_auto = models.CharField(max_length=20, default='', null=True)
    blue_robot3_auto = models.CharField(max_length=20, default='', null=True)
    blue_scale_points = models.SmallIntegerField(default=0, null=True)
    blue_teleop_boulders_high = models.SmallIntegerField(default=0, null=True)
    blue_teleop_boulders_low = models.SmallIntegerField(default=0, null=True)
    blue_teleop_boulders_points = models.SmallIntegerField(default=0, null=True)
    blue_teleop_challenge_points = models.SmallIntegerField(default=0, null=True)
    blue_teleop_crossing_points = models.SmallIntegerField(default=0, null=True)
    blue_tower_captured = models.NullBooleanField(default=False)
    blue_tower_end_strength = models.SmallIntegerField(default=0, null=True)
    blue_tower_faceA = models.CharField(max_length=20, default='', null=True)
    blue_tower_faceB = models.CharField(max_length=20, default='', null=True)
    blue_tower_faceC = models.CharField(max_length=20, default='', null=True)
    red_adjust_points = models.SmallIntegerField(default=0, null=True)
    red_auton_boulders_high = models.SmallIntegerField(default=0, null=True)
    red_auton_boulders_low = models.SmallIntegerField(default=0, null=True)
    red_auton_boulders_points = models.SmallIntegerField(default=0, null=True)
    red_auton_crossing_points = models.SmallIntegerField(default=0, null=True)
    red_auton_reach_points = models.SmallIntegerField(default=0, null=True)
    red_breach_points = models.SmallIntegerField(default=0, null=True)
    red_capture_points = models.SmallIntegerField(default=0, null=True)
    red_defense1 = models.CharField(max_length=20, default='', null=True)
    red_defense2 = models.CharField(max_length=20, default='', null=True)
    red_defense3 = models.CharField(max_length=20, default='', null=True)
    red_defense4 = models.CharField(max_length=20, default='', null=True)
    red_defense1_cross_count = models.SmallIntegerField(default=0, null=True)
    red_defense2_cross_count = models.SmallIntegerField(default=0, null=True)
    red_defense3_cross_count = models.SmallIntegerField(default=0, null=True)
    red_defense4_cross_count = models.SmallIntegerField(default=0, null=True)
    red_defenses_breached = models.NullBooleanField(default=False)
    red_low_bar_cross_count = models.SmallIntegerField(default=0, null=True)
    red_robot1_auto = models.CharField(max_length=20, default='', null=True)
    red_robot2_auto = models.CharField(max_length=20, default='', null=True)
    red_robot3_auto = models.CharField(max_length=20, default='', null=True)
    red_scale_points = models.SmallIntegerField(default=0, null=True)
    red_teleop_boulders_high = models.SmallIntegerField(default=0, null=True)
    red_teleop_boulders_low = models.SmallIntegerField(default=0, null=True)
    red_teleop_boulders_points = models.SmallIntegerField(default=0, null=True)
    red_teleop_challenge_points = models.SmallIntegerField(default=0, null=True)
    red_teleop_crossing_points = models.SmallIntegerField(default=0, null=True)
    red_tower_captured = models.NullBooleanField(default=False)
    red_tower_end_strength = models.SmallIntegerField(default=0, null=True)
    red_tower_faceA = models.CharField(max_length=20, default='', null=True)
    red_tower_faceB = models.CharField(max_length=20, default='', null=True)
    red_tower_faceC = models.CharField(max_length=20, default='', null=True)

    def setup(self, json):
        self.set_json_data(json)

        blue_sb = json['blue']
        red_sb = json['red']

        self.blue_adjust_points = blue_sb['adjustPoints']
        self.blue_auton_boulders_high = blue_sb['autoBouldersHigh']
        self.blue_auton_boulders_low = blue_sb['autoBouldersLow']
        self.blue_auton_boulders_points = blue_sb['autoBoulderPoints']
        self.blue_auton_crossing_points = blue_sb['autoCrossingPoints']
        self.blue_auton_reach_points = blue_sb['autoReachPoints']
        self.blue_auton_score = blue_sb['autoPoints']
        self.blue_breach_points = blue_sb['breachPoints']
        self.blue_capture_points = blue_sb['capturePoints']
        self.blue_defense1 = blue_sb['position2']
        self.blue_defense2 = blue_sb['position3']
        self.blue_defense3 = blue_sb['position4']
        self.blue_defense4 = blue_sb['position5']
        self.blue_defense1_cross_count = blue_sb['position2crossings']
        self.blue_defense2_cross_count = blue_sb['position3crossings']
        self.blue_defense3_cross_count = blue_sb['position4crossings']
        self.blue_defense4_cross_count = blue_sb['position5crossings']
        self.blue_defenses_breached = blue_sb['teleopDefensesBreached']
        self.blue_foul_count = blue_sb['foulCount']
        self.blue_foul_score = blue_sb['foulPoints']
        self.blue_low_bar_cross_count = blue_sb['position1crossings']
        self.blue_robot1_auto = blue_sb['robot1Auto']
        self.blue_robot2_auto = blue_sb['robot2Auto']
        self.blue_robot3_auto = blue_sb['robot3Auto']
        self.blue_scale_points = blue_sb['teleopScalePoints']
        self.blue_teleop_boulders_high = blue_sb['teleopBouldersHigh']
        self.blue_teleop_boulders_low = blue_sb['teleopBouldersLow']
        self.blue_teleop_boulders_points = blue_sb['teleopBoulderPoints']
        self.blue_teleop_challenge_points = blue_sb['teleopChallengePoints']
        self.blue_teleop_crossing_points = blue_sb['teleopCrossingPoints']
        self.blue_tower_captured = blue_sb['teleopTowerCaptured']
        self.blue_tower_end_strength = blue_sb['towerEndStrength']
        self.blue_teleop_score = blue_sb['teleopPoints']
        self.blue_total_score = blue_sb['totalPoints']
        self.blue_tower_faceA = blue_sb['towerFaceA']
        self.blue_tower_faceB = blue_sb['towerFaceB']
        self.blue_tower_faceC = blue_sb['towerFaceC']

        self.red_adjust_points = red_sb['adjustPoints']
        self.red_auton_boulders_high = red_sb['autoBouldersHigh']
        self.red_auton_boulders_low = red_sb['autoBouldersLow']
        self.red_auton_boulders_points = red_sb['autoBoulderPoints']
        self.red_auton_crossing_points = red_sb['autoCrossingPoints']
        self.red_auton_reach_points = red_sb['autoReachPoints']
        self.red_auton_score = red_sb['autoPoints']
        self.red_breach_points = red_sb['breachPoints']
        self.red_capture_points = red_sb['capturePoints']
        self.red_defense1 = red_sb['position2']
        self.red_defense2 = red_sb['position3']
        self.red_defense3 = red_sb['position4']
        self.red_defense4 = red_sb['position5']
        self.red_defense1_cross_count = red_sb['position2crossings']
        self.red_defense2_cross_count = red_sb['position3crossings']
        self.red_defense3_cross_count = red_sb['position4crossings']
        self.red_defense4_cross_count = red_sb['position5crossings']
        self.red_defenses_breached = red_sb['teleopDefensesBreached']
        self.red_foul_count = red_sb['foulCount']
        self.red_foul_score = red_sb['foulPoints']
        self.red_low_bar_cross_count = red_sb['position1crossings']
        self.red_robot1_auto = red_sb['robot1Auto']
        self.red_robot2_auto = red_sb['robot2Auto']
        self.red_robot3_auto = red_sb['robot3Auto']
        self.red_scale_points = red_sb['teleopScalePoints']
        self.red_teleop_boulders_high = red_sb['teleopBouldersHigh']
        self.red_teleop_boulders_low = red_sb['teleopBouldersLow']
        self.red_teleop_boulders_points = red_sb['teleopBoulderPoints']
        self.red_teleop_challenge_points = red_sb['teleopChallengePoints']
        self.red_teleop_crossing_points = red_sb['teleopCrossingPoints']
        self.red_tower_captured = red_sb['teleopTowerCaptured']
        self.red_tower_end_strength = red_sb['towerEndStrength']
        self.red_teleop_score = red_sb['teleopPoints']
        self.red_total_score = red_sb['totalPoints']
        self.red_tower_faceA = red_sb['towerFaceA']
        self.red_tower_faceB = red_sb['towerFaceB']
        self.red_tower_faceC = red_sb['towerFaceC']


class ScoringModel2015(ScoringModel):
    def setup(self, json):
        pass


class ScoringModel2014(ScoringModel):
    def setup(self, json):
        pass
