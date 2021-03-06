from collections import OrderedDict
from typing import Dict, List, Tuple, Set

from bulk_update.manager import BulkUpdateManager
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

from django_mysql.models import Model as MySqlModel, SetCharField

from util.mathutils import solve_linear_least_squares, create_matrix, create_2d_vector


class Team(MySqlModel):
    """
    Attributes:
        
    :attr id: Unique team id, always equal to the team_number.
    :attr active_years {@set[int]}: A set of years that the team has been active (in commission, not participated)
    :attr website {@string}: URL for the team website
    :attr team_number: FRC assigned team number
    :attr name: Long FRC Team Name (note, this can be VERY long, short_name or nickname is recommended)
    :attr short_name: Short FRC Team Name (often the more wel
    :attr nickname: Team Nickname, e.g. Shaker Robotics or Cheesy Poofs
    :attr key: Most specific team name, simply frc#### where #### is the team number
    """
    
    active_years = SetCharField(base_field=models.IntegerField(), max_length=255, default=set())

    website = models.URLField(null=True)
    name = models.TextField(null=True)  # longer name

    locality = models.CharField(max_length=50, null=True)  # e.g. city
    region = models.CharField(max_length=50, null=True)  # e.g. state, province
    country_name = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=150, null=True)  # full city + state + country

    team_number = models.PositiveSmallIntegerField(db_index=True)
    key = models.CharField(max_length=8)  # e.g. frc2791
    nickname = models.CharField(max_length=100, null=True)  # shorter name
    rookie_year = models.PositiveSmallIntegerField(null=True)
    motto = models.TextField(null=True)

    # TrueSkill distribution, which is a model of player skill which assumes a Gaussian distribution with
    # an initial estimate (mean mu, player is assumed to be of average skill) and confidence (standard deviation sigma).
    elo_mu = models.FloatField(default=settings.DEFAULT_MU)
    elo_sigma = models.FloatField(default=settings.DEFAULT_SIGMA)

    objects = BulkUpdateManager()

    # Stats that are too expensive to compute on the fly
    # see util.management.commands.update
    # Yes, it is trivially easy to get some of these through basic querysets. However, this allows us for a much
    # faster lookup at the expense of a very small amount of database space.
    active_event_winstreak = models.PositiveSmallIntegerField(default=0)
    longest_event_winstreak = models.PositiveSmallIntegerField(default=0)
    event_wins_count = models.PositiveSmallIntegerField(default=0)
    event_attended_count = models.PositiveSmallIntegerField(default=0)
    event_winrate = models.FloatField(default=0.0)

    match_wins_count = models.PositiveSmallIntegerField(default=0)
    match_losses_count = models.PositiveSmallIntegerField(default=0)
    match_ties_count = models.PositiveSmallIntegerField(default=0)
    match_winrate = models.FloatField(default=0.0)

    awards_count = models.PositiveSmallIntegerField(default=0)
    blue_banners_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{0} ({1})".format(self.nickname, self.team_number)

    def get_matches(self, year=None) -> QuerySet:

        if year is None:
            return Match.objects.filter(alliances__teams__team_number=self.team_number)
        else:
            return Match.objects.filter(event__year=year).filter(alliances__teams__team_number=self.team_number)

    def get_wins(self, year=None) -> QuerySet:
        matches = Match.objects.prefetch_related('winner__teams')
        if year is None:
            return matches.filter(winner__teams__team_number=self.team_number)
        else:
            matches.select_related('event')
            return matches.filter(event__year=year).filter(winner__teams__team_number=self.team_number)

    def get_losses(self, year=None) -> QuerySet:
        matches = Match.objects.prefetch_related('alliances__teams').select_related('winner')
        if year is None:
            return matches.filter(alliances__teams__team_number=self.team_number).exclude(
                winner__teams__team_number=self.team_number).exclude(winner__isnull=True)
        else:
            matches.select_related('event')
            return matches.filter(event__year=year).filter(
                alliances__teams__team_number=self.team_number).exclude(
                winner__teams__team_number=self.team_number).exclude(winner__isnull=True)

    def get_ties(self, year=None) -> QuerySet:
        matches = Match.objects.prefetch_related('alliances__teams').select_related('winner')
        if year is None:
            return matches.filter(alliances__teams__team_number=self.team_number, winner__isnull=True)
        else:
            matches.select_related('event')
            return matches.filter(event__year=year) \
                .filter(alliances__teams__team_number=self.team_number, winner__isnull=True)

    def get_record(self) -> str:
        return "{0}-{1}-{2}".format(self.match_wins_count, self.match_losses_count, self.match_ties_count)

    def get_winrate(self) -> float:
        return self.match_winrate * 100.0

    def get_elo_standing(self) -> int:
        return Team.objects.filter(elo_mu__gte=self.elo_mu).count()

    def get_awards(self, year=None) -> QuerySet:
        if year is None:
            return Award.objects.filter(recipients=self)
        else:
            return Award.objects.filter(recipients=self, year=year)

    def count_awards_old(self) -> QuerySet:
        return Team.objects.filter(team_number=self.team_number).values_list('award__name'). \
            annotate(count=models.Count('award__award_type')).order_by('-count')

    def count_awards(self) -> Dict[str, List['Event']]:
        awards = {}
        award_types = set(self.award_set.values_list('award_type', flat=True).all())
        types_to_names = {t: Award.choice_to_display(t) for t in award_types}

        # get_events = lambda award_t: Event.objects.filter(award__award_type=award_t, award__recipients=self).values_list(flat=True)
        # This is great if the if statement in the below loop is not required...
        # awards = {types_to_names[t]: get_events(t) for t in award_types}

        for award_t in award_types:
            award = types_to_names[award_t]
            if award not in awards:
                awards[award] = Event.objects.filter(award__award_type=award_t, award__recipients=self).all()

        awards = {k: v for k, v in awards.items() if len(v) > 0}
        return OrderedDict(sorted(awards.items(), key=lambda entry: -len(entry[1])))

    def get_max_opr(self) -> float:
        return self.rankingmodel_set.order_by('-tba_opr').first().tba_opr

    def to_dict(self) -> dict:
        return dict((name, getattr(self, name)) for name in self.__dict__ if not name.startswith('_'))


class Alliance(MySqlModel):
    teams = models.ManyToManyField(Team)

    elo_mu = models.FloatField(default=settings.DEFAULT_MU)
    elo_sigma = models.FloatField(default=settings.DEFAULT_SIGMA)

    objects = BulkUpdateManager()

    def __str__(self):
        return "{0}".format(self.teams.all())

    def get_elo_standing(self) -> int:
        return Alliance.objects.filter(elo_mu__gte=self.elo_mu).count()

    def get_wins(self) -> QuerySet:
        return self.match_set.filter(winner=self)

    def get_losses(self) -> QuerySet:
        return self.match_set.exclude(winner=self).exclude(winner__isnull=True)

    def get_ties(self) -> QuerySet:
        return self.match_set.exclude(winner=self).filter(winner__isnull=True)

    def get_record(self) -> str:
        return "{0}-{1}-{2}".format(self.get_wins().count(), self.get_losses().count(), self.get_ties().count())


class Event(MySqlModel):
    """
    
    :attr id: Unique database id
    :attr key: Unique event key, often of the form ###w where #### is the year and w is the event code
    :attr name: Full event name (e.g. Finger Lakes Regional)
    :attr short_name: Shortened event name (e.g. Finger Lakes)
    :attr event_code: Unique event code (e.g. iri for Indiana Robotics Invitational)
    """
    key = models.CharField(max_length=10, unique=True)  # e.g. 2016cmp
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

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.key == other.key
        else:
            return False

    def has_f3_match(self) -> bool:
        """

        Returns:
            true if the event's finals set went to three games, false otherwise

        """
        return Match.objects.select_related('event') \
            .filter(comp_level__exact='f', match_number__exact=3, event__key__exact=self.key).exists()

    def get_oprs(self) -> Tuple[Tuple[Team, float]]:
        """
        Gets the OPRs for all teams participating in this event, these are returned as (team, opr) tuples.

        Done using the method of linear least squares.
        :return: Tuple of (Team, OPR) pairs
        """

        matches = Match.objects.prefetch_related('red_alliance__teams', 'blue_alliance__teams') \
            .select_related('scoring_model').filter(event=self, comp_level='qm')
        teams = set(Team.objects.filter(event=self).all())      # type: Set[Team]

        # Populate Score Vector
        s_vector = []
        for m in matches:
            s_vector.append(m.scoring_model.red_total_score)
            s_vector.append(m.scoring_model.blue_total_score)

        # Populate Match Matrix, each row consisting of 3 teams, all from either Blue or Red alliance
        m_row_array = []
        if self.year == 2016:
            from TBAW.models import RankingModel2016
            rms = RankingModel2016.objects.select_related('team') \
                .filter(event=self) \
                .annotate(total_contribution=models.F('goals_points') + models.F('auton_points')) \
                .order_by('-total_contribution')

        for match in matches:
            red_teams = set(match.red_alliance.teams.all())
            blue_teams = set(match.blue_alliance.teams.all())

            if self.year == 2016:
                max_contribution = rms.first().total_contribution
                ratios = [rms.get(team=team).c / max_contribution for team in teams]
                contribution_ratios = zip(ratios, teams)
            else:
                contribution_ratios = zip([1.0] * len(teams), teams)

            red_row = [cont_ratio if team in red_teams else 0 for cont_ratio, team in contribution_ratios]
            blue_row = [cont_ratio if team in blue_teams else 0 for cont_ratio, team in contribution_ratios]

            m_row_array.append(red_row)
            m_row_array.append(blue_row)

        # (Eq. 1): [A][OPR] = [SCORE]
        # (Eq. 2): [A]^T[A][OPR] = [A]^T[SCORE], from (Eq. 1)
        #          [P][OPR] = [S], [P] = [A]^T[A] and [S] = [A]^T[SCORE]
        # (Eq. 3): [L][L]^T[OPR] = [S], where [L] is the lower triangular matrix from Cholesky Decomposition of [P]
        # (Eq. 4): [L][y] = [S], [y] = [L]^T[OPR]
        #          Using Forward Substitution to solve for vector [y]
        #
        # [y] is then known, [y] = [L]^T[OPR], [L]^T is an upper triangular matrix,
        # backwards substitute to solve for OPR.
        oprs = solve_linear_least_squares(create_matrix(m_row_array), create_2d_vector(s_vector))
        team_oprs = zip(teams, oprs)    # type: List[Tuple[Team, float]]
        return tuple((team, opr.item(0)) for team, opr in team_oprs)

    def compare_oprs(self):
        from TBAW.models import RankingModel2016
        rms = [rm.team for rm in RankingModel2016.objects.filter(event=self).order_by('-tba_opr')]
        oth = [res[0] for res in self.get_oprs()]

        for i, (tba, frs) in enumerate(zip(rms, oth)):
            print('{0}.) {1},{0}.) {2}'.format(i + 1, tba, frs))


class Match(MySqlModel):
    key = models.CharField(max_length=20,
                           unique=True)  # yyyy{EVENT_CODE}_{COMP_LEVEL}m{MATCH_NUMBER}, e.g. 2016nyro_f1m2
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

    objects = BulkUpdateManager()

    def __str__(self):
        return "{0}".format(self.key)


class Award(MySqlModel):
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
        (1, "Winner"),
        (9, "Engineering Inspiration"),
    )

    non_district_point_choices = (
        (1, "Winner"),
        (2, "Finalist"),
        (3, "Woodie Flowers"),
        (4, "Dean's List"),
        (5, "Volunteer"),
        (14, "Highest Rookie Seed"),
    )

    award_type = models.PositiveSmallIntegerField(choices=award_type_choices)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Team)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{0} - {1} ({2})".format(self.recipients.all(), self.name, self.event)

    @classmethod
    def choice_to_display(cls, choice):
        """

        Args:
            choice: a number inside award_type_choices

        Returns:
            The string associated with the choice. Works the same as some_award.get_award_type_display() but is a
            class method.

        """
        for c in Award.award_type_choices:
            if c[0] == choice:
                return c[1]

        return None


class Robot(MySqlModel):
    key = models.CharField(max_length=13, null=True)  # e.g. frc2791_2016
    team = models.ForeignKey(Team, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    name = models.CharField(max_length=100, null=True)


class AllianceAppearance(MySqlModel):
    alliance = models.ForeignKey(Alliance, null=True)
    event = models.ForeignKey(Event, null=True)

    captain = models.ForeignKey(Team, related_name='captain', null=True)
    first_pick = models.ForeignKey(Team, related_name='first_pick', null=True)
    second_pick = models.ForeignKey(Team, related_name='second_pick', null=True)
    backup = models.ForeignKey(Team, related_name='backup', null=True)

    seed = models.PositiveSmallIntegerField(null=True)
    elo_mu_pre = models.FloatField(null=True)
    elo_mu_post = models.FloatField(null=True)
    elo_sigma_pre = models.FloatField(null=True)
    elo_sigma_post = models.FloatField(null=True)

    objects = BulkUpdateManager()
