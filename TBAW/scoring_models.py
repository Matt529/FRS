from django.db import models
from polymorphic.models import PolymorphicModel


class ScoringModel(PolymorphicModel):
    json_data = models.TextField(default='')

    red_total_score = models.SmallIntegerField()
    red_auton_score = models.SmallIntegerField()
    red_teleop_score = models.SmallIntegerField()
    red_foul_score = models.SmallIntegerField()
    red_foul_count = models.SmallIntegerField(default=-1)

    blue_total_score = models.SmallIntegerField()
    blue_auton_score = models.SmallIntegerField()
    blue_teleop_score = models.SmallIntegerField()
    blue_foul_score = models.SmallIntegerField()
    blue_foul_count = models.SmallIntegerField(default=-1)

    def get_json_data(self):
        import json
        return json.loads(self.json_data)

    def set_json_data(self, data):
        import json
        self.json_data = json.dumps(data)


class ScoringModel2016(ScoringModel):
    # constant point values
    POINTS_AUTON_REACH_DEFENSE = 2
    POINTS_AUTON_CROSS_DEFENSE = 10
    POINTS_AUTON_BOULDER_LOW = 5
    POINTS_AUTON_BOULDER_HIGH = 10
    POINTS_TELEOP_BOULDER_LOW = 2
    POINTS_TELEOP_BOULDER_HIGH = 5

    defense1 = models.CharField(max_length=20)
    defense_1_crossed_count = models.SmallIntegerField()
    defense2 = models.CharField(max_length=20)
    defense_2_cross_count = models.SmallIntegerField()
    defense3 = models.CharField(max_length=20)
    defense_3_crossed_count = models.SmallIntegerField()
    defense4 = models.CharField(max_length=20)
    defense_4_cross_count = models.SmallIntegerField()

    red_breach_points = models.SmallIntegerField()
    red_capture_points = models.SmallIntegerField()
    blue_breach_points = models.SmallIntegerField()
    blue_capture_points = models.SmallIntegerField()

    red_scale_points = models.SmallIntegerField()
    blue_scale_points = models.SmallIntegerField()

    red_auton_boulders_low = models.SmallIntegerField()
    red_auton_boulders_high = models.SmallIntegerField()
    red_auton_boulders_points = models.SmallIntegerField()
    red_teleop_boulders_points = models.SmallIntegerField()

    blue_auton_boulders_low = models.SmallIntegerField()
    blue_auton_boulders_high = models.SmallIntegerField()
    blue_auton_boulders_points = models.SmallIntegerField()
    blue_teleop_boulders_points = models.SmallIntegerField()

    red_auton_crossing_points = models.SmallIntegerField()
    red_auton_reach_points = models.SmallIntegerField()
    red_teleop_crossing_points = models.SmallIntegerField()
    blue_auton_crossing_points = models.SmallIntegerField()
    blue_auton_reach_points = models.SmallIntegerField()
    blue_teleop_crossing_points = models.SmallIntegerField()


class ScoringModel2015(ScoringModel):
    pass


class ScoringModel2014(ScoringModel):
    pass

# etc
