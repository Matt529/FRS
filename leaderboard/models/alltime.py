from TBAW.models import Team, Award, Alliance
from django.db.models import Count, F, ExpressionWrapper, FloatField, When, Case, Sum, PositiveSmallIntegerField


class AllianceLeaderboard:
    @staticmethod
    def most_match_wins_3(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which combinations of 3 teams have the most match wins together.

        """
        return Alliance.objects.annotate(stat=Count('winner')).order_by('-stat')[:n]

    @staticmethod
    def most_match_wins_2(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which combinations of 2 teams have the most match wins together.

        """
        # matches = Match.objects.filter(winner__isnull=False)
        # count = Counter()
        # for match in matches:
        #     combos = combinations(match.winner.teams.all(), 2)
        #     for combo in combos:
        #         count[combo] += 1
        #
        # return count.most_common() if n is None else count.most_common(n)
        raise NotImplementedError

    @staticmethod
    def most_event_wins_3(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which combinations of 3 teams have the most event wins together (ie won the finals).

        """
        return Alliance.objects.annotate(stat=Count('winning_alliance')).order_by('-stat')[:n]

    @staticmethod
    def most_event_wins_2(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which combinations of 2 teams have the most event wins together (ie won the finals).

        """
        # winning_alliances = AllianceLeaderboard.most_event_wins_3(get_counter_obj=True)
        # count = Counter()
        # for alliance in winning_alliances.most_common():
        #     teams = alliance[0].teams.all()
        #     combos = combinations(teams, 2)
        #     for combo in set(combos):
        #         if set(combo).issubset(set(teams)):
        #             count[combo] += 1
        #
        # return count.most_common() if n is None else count.most_common(n)

        raise NotImplementedError


class TeamLeaderboard:
    @staticmethod
    def most_match_wins(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the most match wins. Has the extra field 'stat'.

        """
        return Team.objects.annotate(stat=Count('alliance__winner')).order_by('-stat')[:n]

    @staticmethod
    def most_event_wins(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the most event wins. Has the extra field 'stat'.

        """
        return Team.objects.annotate(stat=Count('alliance__winning_alliance',
                                                distinct=True)).order_by('-stat')[:n]

    @staticmethod
    def highest_win_rate(n=None):
        """
        1. Counts how many times a team has appeared on an alliance and saves it to a float named num_played
        2. Counts how many times a team has appeared on a winning alliance and saves it to a float named num_wins
        3. Divides num_wins by num_played and saves it to a float named win_rate
        4. Orders the teams by win_rate

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the highest winrate. Has the extra field 'stat'.
        """
        return Team.objects.annotate(
            num_played=ExpressionWrapper(Count('alliance__match', distinct=True), output_field=FloatField()),
            num_wins=ExpressionWrapper(Count('alliance__winner', distinct=True), output_field=FloatField())
        ).annotate(
            stat=ExpressionWrapper(F('num_wins') * 100.0 / F('num_played'), output_field=FloatField())
        ).order_by('-stat')[:n]

    @staticmethod
    def highest_elo(n=None):
        """

        Args:
            n:  An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the highest Elo rating. Has the extra field 'stat'.

        """
        return Team.objects.order_by('-elo_mu').annotate(stat='elo_mu')[:n]

    @staticmethod
    def highest_elo_scaled(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the highest Elo rating (scaled to start at 1500 rather than 25).

        """
        return Team.objects.annotate(stat=F('elo_mu') * 60).order_by('-stat')[:n]

    @staticmethod
    def most_award_wins(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A query set of which teams have the most total awards. Has the extra field 'stat'.


        """
        return Team.objects.annotate(stat=Count('award')).order_by('-stat')[:n]

    @staticmethod
    def most_blue_banners(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A query set of which teams have the most blue banners. Has the extra field 'stat'.

        """
        blue_banner_reverse = dict((v, k) for k, v in Award.blue_banner_choices)
        return Team.objects.filter(award__award_type__in=blue_banner_reverse.values()).annotate(
            stat=Sum(
                Case(
                    When(award__award_type__in=blue_banner_reverse.values(), then=1),
                    default=0,
                    output_field=PositiveSmallIntegerField(),
                )
            )
        ).order_by('-stat')[:n]
