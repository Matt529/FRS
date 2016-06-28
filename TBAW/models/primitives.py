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

    def get_matches(self):
        return Match.objects.filter(alliances__teams__team_number=self.team_number)


class Alliance(models.Model):
    teams = models.ManyToManyField(Team)
    color = models.CharField(max_length=4, null=True)

    def __str__(self):
        return "{0}".format(self.teams.all())

    def to_html(self):
        return "{0}\n{1}\n{2}".format(self.teams.first(), self.teams.all()[1], self.teams.all()[2])


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

    blue_alliance = models.ForeignKey(Alliance, null=True, related_name='blue_alliance')
    red_alliance = models.ForeignKey(Alliance, null=True, related_name='red_alliance')
    winner = models.ForeignKey(Alliance, null=True, related_name='winner')
    scoring_model = models.ForeignKey('TBAW.ScoringModel', null=True)

    def __str__(self):
        return "{0}".format(self.key)


class Award(models.Model):
    name = models.CharField(max_length=150)

    # https://github.com/the-blue-alliance/the-blue-alliance/blob/master/consts/award_type.py#L15
    award_type_choices = (
        (0, "Chairman's"),
        (1, "Winner"),
        (2, "Finalist"),
        (3, "Woodie Flowers"),
        (4, "Dean's List"),
        (5, "Volunteer"),
        (6, "Founders"),
        (7, "Bart Kamen Memorial"),
        (8, "Make It Loud"),
        (9, "Engineering Inspiration"),
        (10, "Rookie All Star"),
        (11, "Gracious Professionalism"),
        (12, "Coopertition"),
        (13, "Judges"),
        (14, "Highest Rookie Seed"),
        (15, "Rookie Inspiration"),
        (16, "Industrial Design"),
        (17, "Quality"),
        (18, "Safety"),
        (19, "Sportsmanship"),
        (20, "Creativity"),
        (21, "Engineering Excellence"),
        (22, "Entrepreneurship"),
        (23, "Excellence in Design"),
        (24, "Excellence in Design (CAD)"),
        (25, "Excellence in Design (Animation)"),
        (26, "Driving Tomorrow's Technology"),
        (27, "Imagery"),
        (28, "Media and Technology"),
        (29, "Innovation in Control"),
        (30, "Spirit"),
        (31, "Website"),
        (32, "Visualization"),
        (33, "Autodesk Inventor"),
        (34, "Future Innovator"),
        (35, "Recognition of Extraordinary Service"),
        (36, "Outstanding Cart"),
        (37, "WSU Aim Higher"),
        (38, "Leadership in Control"),
        (39, "Number 1 Seed"),
        (40, "Incredible Play"),
        (41, "People's Choice Animation"),
        (42, "Rising Star Visualization"),
        (43, "Best Offensive Round"),
        (44, "Best Play of the Day"),
        (45, "Featherweight in the Finals"),
        (46, "Most Photogenic"),
        (47, "Outstanding Defense"),
        (48, "Power to Simplify"),
        (49, "Against All Odds"),
        (50, "Rising Star"),
        (51, "Chairman's Honorable Mention"),
        (52, "Content Communication Honorable Mention"),
        (53, "Technical Execution Honorable Mention"),
        (54, "Realization"),
        (55, "Realization Honorable Mention"),
        (56, "Design Your Future"),
        (57, "Design Your Future Honorable Mention"),
        (58, "Special Recognition Character Animation"),
        (59, "High Score"),
        (60, "Teacher Pioneer"),
        (61, "Best Craftsmanship"),
        (62, "Best Defensive Match"),
        (63, "Play of the Day"),
        (64, "Programming"),
        (65, "Professionalism"),
        (66, "Golden Corndog"),
        (67, "Most Improved Team"),
        (68, "Wildcard"),
    )

    blue_banner_choices = (
        (0, "Chairman's"),
        (1, "Winner")
    )

    non_district_point_choices = (
        (1, "Winner"),
        (2, "Finalist"),
        (3, "Woodie Flowers"),
        (4, "Dean's List"),
        (5, "Volunteer"),
        (14, "Highest Rookie Seed"),
    )

    award_type = models.CharField(choices=award_type_choices, max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Team)
    year = models.PositiveSmallIntegerField()


class Robot(models.Model):
    key = models.CharField(max_length=13, null=True)  # e.g. frc2791_2016
    team = models.ForeignKey(Team, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    name = models.CharField(max_length=100, null=True)


class AllianceAppearance(models.Model):
    alliance = models.ForeignKey(Alliance, null=True)
    event = models.ForeignKey(Event, null=True)
    seed = models.PositiveSmallIntegerField(null=True)
