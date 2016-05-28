from django.db import models

MAX_NAME_LENGTH = 120
MAX_DESCRIPTION_LENGTH = 500


class Team(models.Model):
    website = models.URLField()
    name = models.TextField()  # longer name

    locality = models.CharField(max_length=MAX_NAME_LENGTH)  # e.g. city
    region = models.CharField(max_length=MAX_NAME_LENGTH)  # e.g. state, province
    country_name = models.CharField(max_length=MAX_NAME_LENGTH)
    location = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)  # full city + state + country

    team_number = models.PositiveIntegerField()
    key = models.CharField(max_length=8)  # e.g. frc2791
    nickname = models.CharField(max_length=MAX_NAME_LENGTH)  # shorter name
    rookie_year = models.PositiveIntegerField()
    motto = models.TextField()

    def __str__(self):
        return "{0} ({1})".format(self.name, self.team_number)

    @classmethod
    def create(cls, website, name, locality, region, country_name, location, team_number, key, nickname, rookie_year,
               motto):
        team = cls(website=website, name=name, locality=locality, region=region, country_name=country_name,
                   location=location, team_number=team_number, key=key, nickname=nickname, rookie_year=rookie_year,
                   motto=motto)
        team.save()
        return team


class Event(models.Model):
    key = models.CharField(max_length=10)  # e.g. 2016cmp
    name = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)  # e.g. Finger Lakes Regional
    short_name = models.CharField(null=True, max_length=MAX_NAME_LENGTH)  # e.g. Finger Lakes
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
    event_type = models.IntegerField(choices=event_type_choices)

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
    event_district = models.IntegerField(choices=event_district_choices)

    year = models.PositiveIntegerField()
    location = models.CharField(max_length=MAX_NAME_LENGTH)
    venue_address = models.TextField()
    timezone = models.CharField(max_length=20)
    website = models.URLField(null=True)
    official = models.BooleanField()

    # teams = models.ManyToManyField(Team)

    # webcast = my_webcast_model(), parse JSON data to model fields

    # alliances = models.ManyToManyField(Alliance, null=True)

    # district_points = my_district_points_model(), parse JSON data to model fields


class Match(models.Model):
    key = models.CharField(max_length=20)  # yyyy{EVENT_CODE}_{COMP_LEVEL}m{MATCH_NUMBER}
    comp_level = models.CharField(max_length=6)  # e.g. qm, ef, qf, sf, f

    """The set number in a series of matches where more than one match is required in the match series.
    2010sc_qf1m2, would be match 2 in quarter finals 1.
    -The Blue Alliance"""
    set_number = models.CharField(null=True, max_length=20)

    match_number = models.CharField(max_length=20)  # e.g. 2016nyro_qm20
    # alliances = models.ManyToManyField(Alliance)
    # score_breakdown = my_score_model(null=true), parse JSON data to model fields
    # videos = my_videos_model, parse JSON data to model fields
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    time_string = models.CharField(max_length=25)
    # time = models.DateTimeField(), parse UNIX timestamp to DatetimeField


class Award(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)

    # todo: https://github.com/the-blue-alliance/the-blue-alliance/blob/master/consts/award_type.py#L15
    award_type_choices = ()

    award_type = models.CharField(choices=award_type_choices, max_length=MAX_NAME_LENGTH)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # recipient = models.ForeignKey(Team, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()


class Robot(models.Model):
    key = models.CharField(max_length=13)  # e.g. frc2791_2016
    # team = models.ForeignKey(Team, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    name = models.CharField(max_length=MAX_NAME_LENGTH)


class Alliance(models.Model):
    # teams = models.ManyToManyField(Team)
    pass
