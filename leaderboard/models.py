from itertools import combinations

from TBAW.models import Match, Alliance, Team
from collections import Counter


class AllianceLeaderboard:
    @staticmethod
    def most_match_wins():
        matches = Match.objects.all()
        count = Counter()
        for match in matches:
            count[match.winner] += 1
        # Remove ties
        del count[None]
        return count
    @staticmethod
    def most_event_wins_3():
        matches_of_3 = Match.objects.filter(comp_level__exact='f', match_number__exact=3)
        count = Counter()
        for match in matches_of_3:
            count[match.winner] += 1

        # need to have a better filter, currently double counting match 2 and match 3
        matches_of_2 = [x for x in Match.objects.filter(comp_level__exact='f', match_number=2, match_number=3) if
                        x not in matches_of_3]
        for match in matches_of_2:
            count[match.winner] += 1
        return count
    @staticmethod
    def most_event_wins_2():
        winning_alliances = AllianceLeaderboard.most_event_wins_3()
        count = Counter()
        for alliance in winning_alliances:
            teams = alliance.teams.all()
            combos = combinations(teams, 2)
            for combo in combos:
                if set(combo).issubset(set(alliance.teams.all())):
                    count[combo] += 1
        return count


class TeamLeaderboard:
    @staticmethod
    def most_match_wins():
        matches = Match.objects.all()
        count = Counter()
        for m in matches:
            if m.winner is None:
                continue
            for team in m.winner.teams.all():
                count[team] += 1
        return count

    @staticmethod
    def most_event_wins():
        matches_of_3 = Match.objects.filter(comp_level__exact='f', match_number__exact=3)
        count = Counter()
        for match in matches_of_3:
            if match.winner is None:
                continue
            for team in match.winner.teams.all():
                count[team] += 1
        matches_of_2 = [x for x in Match.objects.filter(comp_level__exact='f', match_number__exact=2) if
                        x not in matches_of_3]
        for match in matches_of_2:
            if match.winner is None:
                continue
            for team in match.winner.teams.all():
                count[team] += 1
        return count
