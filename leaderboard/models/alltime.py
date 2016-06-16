from itertools import combinations

from TBAW.models import Match, Team, Award
from collections import Counter
from django.db.models import Count, F, ExpressionWrapper, FloatField, When, Case, Sum, PositiveSmallIntegerField
from util.check import event_has_f3_match


class AllianceLeaderboard:
    @staticmethod
    def most_match_wins_3(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which combinations of 3 teams have the most match wins together.

        """
        matches = Match.objects.filter(winner__isnull=False)
        count = Counter()
        for match in matches:
            count[match.winner] += 1
        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def most_match_wins_2(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which combinations of 2 teams have the most match wins together.

        """
        matches = Match.objects.filter(winner__isnull=False)
        count = Counter()
        for match in matches:
            combos = combinations(match.winner.teams.all(), 2)
            for combo in combos:
                count[combo] += 1

        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def most_event_wins_3(n=None, get_counter_obj=False):
        """

        Args:
            n: An optional argument that cuts the return to n elements.
            get_counter_obj: This is just a helper argument for the most_event_wins_2 function.

        Returns:
            A list of which combinations of 3 teams have the most event wins together (ie won the finals).

        """
        matches_of_3 = Match.objects.filter(comp_level__exact='f', match_number__exact=3)
        count = Counter()
        for match in matches_of_3:
            count[match.winner] += 1

        matches_of_2 = [x for x in Match.objects.filter(comp_level__exact='f', match_number__exact=2) if
                        not event_has_f3_match(x.event.key)]

        for match in matches_of_2:
            count[match.winner] += 1

        del count[None]
        return (count.most_common() if n is None else count.most_common(n)) if get_counter_obj is False else count

    @staticmethod
    def most_event_wins_2(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which combinations of 2 teams have the most event wins together (ie won the finals).

        """
        winning_alliances = AllianceLeaderboard.most_event_wins_3(get_counter_obj=True)
        count = Counter()
        for alliance in winning_alliances:
            teams = alliance.teams.all()
            combos = combinations(teams, 2)
            for combo in combos:
                if set(combo).issubset(set(alliance.teams.all())):
                    count[combo] += 1

        return count.most_common() if n is None else count.most_common(n)


class TeamLeaderboard:
    @staticmethod
    def most_match_wins(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the most match wins.

        """
        return Team.objects.annotate(num_wins=Count('alliance__winner')).order_by('-num_wins')[:n]

    @staticmethod
    def most_event_wins(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the most event wins.

        """
        return Team.objects.annotate(num_wins=Count('alliance__winning_alliance',
                                                    distinct=True)).order_by('-num_wins')[:n]

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
            A list of which teams have the highest winrate.
        """
        return Team.objects.annotate(
            num_played=ExpressionWrapper(Count('alliance__match', distinct=True), output_field=FloatField()),
            num_wins=ExpressionWrapper(Count('alliance__winner', distinct=True), output_field=FloatField())
        ).annotate(
            win_rate=ExpressionWrapper(F('num_wins') * 1.0 / F('num_played'), output_field=FloatField())
        ).order_by('-win_rate')[:n]

    @staticmethod
    def highest_elo(n=None):
        """

        Args:
            n:  An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the highest Elo rating.

        """
        return Team.objects.order_by('-elo_mu')[:n]

    @staticmethod
    def highest_elo_scaled(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A list of which teams have the highest Elo rating (scaled to start at 1500 rather than 25).

        """
        return Team.objects.annotate(elo_scaled=F('elo_mu') * 60).order_by('-elo_scaled')[:n]

    @staticmethod
    def most_award_wins(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A query set of which teams have the most total awards. Has the extra field 'num_awards'.


        """
        return Team.objects.annotate(num_awards=Count('award')).order_by('-num_awards')[:n]

    @staticmethod
    def most_blue_banners(n=None):
        """

        Args:
            n: An optional argument that cuts the return to n elements.

        Returns:
            A query set of which teams have the most blue banners. Has the extra field 'num_blue_banners'.

        """
        blue_banner_reverse = dict((v, k) for k, v in Award.blue_banner_choices)
        return Team.objects.filter(award__award_type__in=blue_banner_reverse.values()).annotate(
            num_blue_banners=Sum(
                Case(
                    When(award__award_type__in=blue_banner_reverse.values(), then=1),
                    default=0,
                    output_field=PositiveSmallIntegerField(),
                )
            )
        ).order_by('-num_blue_banners')[:n]
