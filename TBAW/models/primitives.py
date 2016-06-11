from FRS.settings import DEFAULT_MU, DEFAULT_SIGMA
from django.db import models
from util.computations import average_match_score


class Team(models.Model):
    website = models.URLField(null=True)
    name = models.TextField()  # longer name

    locality = models.CharField(max_length=50, null=True)  # e.g. city
    region = models.CharField(max_length=50, null=True)  # e.g. state, province
    country_name = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=150, null=True)  # full city + state + country

    team_number = models.PositiveSmallIntegerField()
    key = models.CharField(max_length=8)  # e.g. frc2791
    nickname = models.CharField(max_length=100)  # shorter name
    rookie_year = models.PositiveSmallIntegerField(null=True)
    motto = models.TextField(null=True)

    # Modeled after TrueSkill, which is a Gaussian distribution with mu=25.0 and sigma = 25/3.
    elo_mu = models.FloatField(default=DEFAULT_MU)
    elo_sigma = models.FloatField(default=DEFAULT_SIGMA)

    def __str__(self):
        return "{0} ({1})".format(self.nickname, self.team_number)


class Alliance(models.Model):
    # is this necessary? idk
    color_choices = (
        ('Red', 'Red'),
        ('Blue', 'Blue')
    )
    teams = models.ManyToManyField(Team)
    color = models.CharField(max_length=4, choices=color_choices, null=True)
    seed = models.SmallIntegerField(default=0, null=True)

    def __str__(self):
        return "Alliance (#{1}) {0}".format(self.teams.all(), self.seed)


class Event(models.Model):
    key = models.CharField(max_length=10)  # e.g. 2016cmp
    name = models.CharField(max_length=100)  # e.g. Finger Lakes Regional
    short_name = models.CharField(null=True, max_length=50)  # e.g. Finger Lakes
    event_code = models.CharField(max_length=7)  # e.g. cmp

    """https://github.com/the-blue-alliance/the-blue-alliance/blob/master/consts/event_type.py"""
    event_type_choices = (
        (0, 'Regional'),
        (1, 'District'),
        (2, 'District Championship'),
        (3, 'Championship Division'),
        (4, 'Championship Finals'),
        (99, 'Offseason'),
        (100, 'Preseason'),
        (-1, 'Unlabeled')
    )
    event_type = models.SmallIntegerField(choices=event_type_choices, null=True)

    """https://github.com/the-blue-alliance/the-blue-alliance/blob/master/consts/district_type.py#L6"""
    event_district_choices = (
        (0, 'No District'),
        (1, 'Michigan'),
        (2, 'Mid-Atlantic'),
        (3, 'New England'),
        (4, 'Pacific Northwest'),
        (5, 'Indiana'),
        (6, 'Chesapeake'),
        (7, 'North Carolina'),
        (8, 'Georgia'),
    )
    event_district = models.SmallIntegerField(choices=event_district_choices, null=True)

    year = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=50, null=True)
    venue_address = models.TextField(null=True)
    timezone = models.CharField(max_length=35, null=True)
    website = models.URLField(null=True)
    official = models.BooleanField()
    teams = models.ManyToManyField(Team)
    alliances = models.ManyToManyField(Alliance)
    end_date = models.DateField(null=True)
    winning_alliance = models.ForeignKey(Alliance, related_name='winning_alliance', null=True)

    # webcast = my_webcast_model(), parse JSON data to model fields
    # district_points = my_district_points_model(), parse JSON data to model fields

    def __str__(self):
        return "{0}".format(self.key)

    def get_average_qual_match_score(self):
        return average_match_score(self.match_set.filter(comp_level__exact='qm'))

    def get_average_playoff_match_score(self):
        return average_match_score(self.match_set.filter(comp_level__in=['ef', 'qf', 'sf', 'f']))

    def get_average_overall_match_score(self):
        return average_match_score(self.match_set.all())


class Match(models.Model):
    key = models.CharField(max_length=20)  # yyyy{EVENT_CODE}_{COMP_LEVEL}m{MATCH_NUMBER}, e.g. 2016nyro_f1m2
    comp_level = models.CharField(max_length=6)  # e.g. qm, ef, qf, sf, f
    set_number = models.CharField(null=True, max_length=20)  # in 2016nyro_qf3m2, the set number is 3

    match_number = models.CharField(max_length=20)  # e.g. 2016nyro_qm20
    alliances = models.ManyToManyField(Alliance)
    # videos = my_videos_model, parse JSON data to model fields
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # time_string = models.CharField(max_length=25)
    # time = models.DateTimeField(), parse UNIX timestamp to DatetimeField

    winner = models.ForeignKey(Alliance, null=True, related_name='winner')
    scoring_model = models.ForeignKey('TBAW.ScoringModel', null=True)

    def __str__(self):
        return "{0}".format(self.key)


class Award(models.Model):
    name = models.CharField(max_length=100)

    # todo: https://github.com/the-blue-alliance/the-blue-alliance/blob/master/consts/award_type.py#L15
    award_type_choices = ()

    award_type = models.CharField(choices=award_type_choices, max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # recipient = models.ForeignKey(Team, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()


class Robot(models.Model):
    key = models.CharField(max_length=13, null=True)  # e.g. frc2791_2016
    team = models.ForeignKey(Team, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
