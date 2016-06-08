from itertools import combinations

from TBAW.models import Match, Team
from collections import Counter
from operator import itemgetter
from util.check import event_has_f3_match


class AllianceLeaderboard:
    @staticmethod
    def most_match_wins_3(n=None):
        matches = Match.objects.filter(winner__isnull=False)
        count = Counter()
        for match in matches:
            count[match.winner] += 1
        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def most_match_wins_2(n=None):
        matches = Match.objects.filter(winner__isnull=False)
        count = Counter()
        for match in matches:
            combos = combinations(match.winner.teams.all(), 2)
            for combo in combos:
                count[combo] += 1

        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def most_event_wins_3(n=None, get_counter_obj=False):
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
        matches = Match.objects.filter(winner__isnull=False)
        count = Counter()
        for m in matches:
            for team in m.winner.teams.all():
                count[team] += 1

        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def most_match_wins_x(n=None):
        d = {}
        for team in Team.objects.filter(alliance__isnull=False):
            d[team] = Match.objects.filter(winner__in=team.alliance_set.all()).count()

        return sorted(d.items(), key=itemgetter(1))[:n]

    @staticmethod
    def most_event_wins(n=None):
        matches_of_3 = Match.objects.filter(comp_level__exact='f', match_number__exact=3, winner__isnull=False)
        count = Counter()
        for match in matches_of_3:
            for team in match.winner.teams.all():
                count[team] += 1
        matches_of_2 = [x for x in Match.objects.filter(comp_level__exact='f', match_number__exact=2, winner__isnull=False) if
                        not event_has_f3_match(x.event.key)]
        for match in matches_of_2:
            for team in match.winner.teams.all():
                count[team] += 1

        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def highest_win_rate(n=None):
        matches = Match.objects.filter(winner__isnull=False)
        wins = Counter()
        total = Counter()
        for match in matches:
            for alliance in match.alliances.all():
                for team in alliance.teams.all():
                    total[team] += 1

            for team in match.winner.teams.all():
                wins[team] += 1

        for key, value in total.most_common():
            if total[key] >= 14:
                total[key] = wins[key] / total[key]
            else:
                del total[key]

        return total.most_common() if n is None else total.most_common(n)
