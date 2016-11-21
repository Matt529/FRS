from abc import ABCMeta, abstractmethod

from django.db import models
from polymorphic.models import PolymorphicModel


class ScoringModel(PolymorphicModel):
    __metaclass__ = ABCMeta

    red_total_score = models.SmallIntegerField(null=True)
    blue_total_score = models.SmallIntegerField(null=True)

    def get_higher_score(self) -> int:
        return self.red_total_score if self.red_total_score > self.blue_total_score else self.blue_total_score

    @abstractmethod
    def setup(self, json):
        return

    def matrix(self):
        from TBAW.models import Match, Team
        import numpy as np

        matches = Match.objects.filter(event__key='2016nyro')
        teams = Team.objects.filter(event__key='2016nyro')
        team_tuples = []
        i = 0
        for t in teams:
            team_tuples.append((i, t))
            i += 1

        b = [m.scoring_model.red_total_score for m in matches]
        a = [[0 for i in range(matches.count())] for j in range(matches.count())]

        for count, match_row in enumerate(matches):
            for team in team_tuples:
                if team[1] in match_row.red_alliance.teams.all():
                    a[count][team[0]] = 1

        x = np.linalg.solve(a, b)


    def __str__(self):
        return "{0} (B: {1}, R: {2})".format(self.match_set.first(), self.blue_total_score, self.red_total_score)

    def get_percentile(self, *args):
        max_value_sum = 0
        self_value_sum = 0
        for field in args:
            if hasattr(self, field):
                max_value_sum += getattr(type(self).objects.order_by('-{}'.format(field)).first(), field)
                self_value_sum += getattr(self, field)
            else:
                raise AttributeError("ScoringModel does not contain field {}".format(field))

        return self_value_sum / max_value_sum


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

    blue_auton_score = models.SmallIntegerField(default=0, null=True)
    blue_teleop_score = models.SmallIntegerField(default=0, null=True)
    blue_foul_score = models.SmallIntegerField(default=0, null=True)
    blue_foul_count = models.SmallIntegerField(default=0, null=True)
    blue_tech_foul_count = models.SmallIntegerField(default=0, null=True)

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

    red_auton_score = models.SmallIntegerField(default=0, null=True)
    red_teleop_score = models.SmallIntegerField(default=0, null=True)
    red_foul_score = models.SmallIntegerField(default=0, null=True)
    red_foul_count = models.SmallIntegerField(default=0, null=True)
    red_tech_foul_count = models.SmallIntegerField(default=0, null=True)

    def setup(self, json):
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
    coopertition = models.TextField(max_length=7, null=True)

    blue_tote_count_far = models.PositiveSmallIntegerField(default=0, null=True)
    blue_tote_count_near = models.PositiveSmallIntegerField(default=0, null=True)
    blue_tote_set = models.NullBooleanField(default=False)
    blue_container_set = models.NullBooleanField(default=False)
    blue_container_points = models.PositiveSmallIntegerField(default=0, null=True)
    blue_container_count_1 = models.PositiveSmallIntegerField(default=0, null=True)
    blue_container_count_2 = models.PositiveSmallIntegerField(default=0, null=True)
    blue_container_count_3 = models.PositiveSmallIntegerField(default=0, null=True)
    blue_container_count_4 = models.PositiveSmallIntegerField(default=0, null=True)
    blue_container_count_5 = models.PositiveSmallIntegerField(default=0, null=True)
    blue_container_count_6 = models.PositiveSmallIntegerField(default=0, null=True)
    blue_litter_count_unprocessed = models.PositiveSmallIntegerField(default=0, null=True)
    blue_litter_count_container = models.PositiveSmallIntegerField(default=0, null=True)
    blue_litter_count_landfill = models.PositiveSmallIntegerField(default=0, null=True)
    blue_litter_points = models.PositiveSmallIntegerField(default=0, null=True)
    blue_tote_points = models.PositiveSmallIntegerField(default=0, null=True)
    blue_tote_stack = models.NullBooleanField(default=False)
    blue_robot_set = models.NullBooleanField(default=False)

    blue_auton_score = models.SmallIntegerField(default=0, null=True)
    blue_teleop_score = models.SmallIntegerField(default=0, null=True)
    blue_foul_score = models.SmallIntegerField(default=0, null=True)
    blue_foul_count = models.SmallIntegerField(default=0, null=True)

    red_tote_count_far = models.PositiveSmallIntegerField(default=0, null=True)
    red_tote_count_near = models.PositiveSmallIntegerField(default=0, null=True)
    red_tote_set = models.NullBooleanField(default=False)
    red_container_set = models.NullBooleanField(default=False)
    red_container_points = models.PositiveSmallIntegerField(default=0, null=True)
    red_container_count_1 = models.PositiveSmallIntegerField(default=0, null=True)
    red_container_count_2 = models.PositiveSmallIntegerField(default=0, null=True)
    red_container_count_3 = models.PositiveSmallIntegerField(default=0, null=True)
    red_container_count_4 = models.PositiveSmallIntegerField(default=0, null=True)
    red_container_count_5 = models.PositiveSmallIntegerField(default=0, null=True)
    red_container_count_6 = models.PositiveSmallIntegerField(default=0, null=True)
    red_litter_count_unprocessed = models.PositiveSmallIntegerField(default=0, null=True)
    red_litter_count_container = models.PositiveSmallIntegerField(default=0, null=True)
    red_litter_count_landfill = models.PositiveSmallIntegerField(default=0, null=True)
    red_litter_points = models.PositiveSmallIntegerField(default=0, null=True)
    red_tote_points = models.PositiveSmallIntegerField(default=0, null=True)
    red_tote_stack = models.NullBooleanField(default=False)
    red_robot_set = models.NullBooleanField(default=False)

    red_auton_score = models.SmallIntegerField(default=0, null=True)
    red_teleop_score = models.SmallIntegerField(default=0, null=True)
    red_foul_score = models.SmallIntegerField(default=0, null=True)
    red_foul_count = models.SmallIntegerField(default=0, null=True)

    def setup(self, json):
        self.coopertition = json['coopertition']
        blue_sb = json['blue']
        red_sb = json['red']

        self.blue_total_score = blue_sb['total_points']
        self.blue_auton_score = blue_sb['auto_points']
        self.blue_teleop_score = blue_sb['teleop_points']
        self.blue_foul_score = blue_sb['foul_points']
        self.blue_foul_count = blue_sb['foul_count']
        self.blue_tote_count_far = blue_sb['tote_count_far']
        self.blue_tote_count_near = blue_sb['tote_count_near']
        self.blue_tote_set = blue_sb['tote_set']
        self.blue_container_set = blue_sb['container_set']
        self.blue_container_points = blue_sb['container_points']
        self.blue_container_count_1 = blue_sb['container_count_level1']
        self.blue_container_count_2 = blue_sb['container_count_level2']
        self.blue_container_count_3 = blue_sb['container_count_level3']
        self.blue_container_count_4 = blue_sb['container_count_level4']
        self.blue_container_count_5 = blue_sb['container_count_level5']
        self.blue_container_count_6 = blue_sb['container_count_level6']
        self.blue_litter_count_unprocessed = blue_sb['litter_count_unprocessed']
        self.blue_litter_count_container = blue_sb['litter_count_container']
        self.blue_litter_count_landfill = blue_sb['litter_count_landfill']
        self.blue_litter_points = blue_sb['litter_points']
        self.blue_tote_points = blue_sb['tote_points']
        self.blue_tote_stack = blue_sb['tote_stack']
        self.blue_robot_set = blue_sb['robot_set']

        self.red_total_score = red_sb['total_points']
        self.red_auton_score = red_sb['auto_points']
        self.red_teleop_score = red_sb['teleop_points']
        self.red_foul_score = red_sb['foul_points']
        self.red_foul_count = red_sb['foul_count']
        self.red_tote_count_far = red_sb['tote_count_far']
        self.red_tote_count_near = red_sb['tote_count_near']
        self.red_tote_set = red_sb['tote_set']
        self.red_container_set = red_sb['container_set']
        self.red_container_points = red_sb['container_points']
        self.red_container_count_1 = red_sb['container_count_level1']
        self.red_container_count_2 = red_sb['container_count_level2']
        self.red_container_count_3 = red_sb['container_count_level3']
        self.red_container_count_4 = red_sb['container_count_level4']
        self.red_container_count_5 = red_sb['container_count_level5']
        self.red_container_count_6 = red_sb['container_count_level6']
        self.red_litter_count_unprocessed = red_sb['litter_count_unprocessed']
        self.red_litter_count_container = red_sb['litter_count_container']
        self.red_litter_count_landfill = red_sb['litter_count_landfill']
        self.red_litter_points = red_sb['litter_points']
        self.red_tote_points = red_sb['tote_points']
        self.red_tote_stack = red_sb['tote_stack']
        self.red_robot_set = red_sb['robot_set']

        # https://github.com/the-blue-alliance/the-blue-alliance/issues/1563
        if self.blue_tote_count_far < 0:
            self.blue_tote_count_far = 0
