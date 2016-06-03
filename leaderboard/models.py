from itertools import combinations

from TBAW.models import Match, Alliance, Team, Event
from collections import Counter
from operator import itemgetter
from util.check import event_has_f3_match


class AllianceLeaderboard:
    @staticmethod
    def most_match_wins_3(n=None):
        matches = Match.objects.all()
        count = Counter()
        for match in matches:
            count[match.winner] += 1
        # Remove ties
        del count[None]
        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def most_match_wins_2(n=None):
        matches = Match.objects.all()
        count = Counter()
        for match in matches:
            if match.winner is None:
                continue
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
        matches = Match.objects.all()
        count = Counter()
        for m in matches:
            if m.winner is None:
                continue
            for team in m.winner.teams.all():
                count[team] += 1

        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def most_event_wins(n=None):
        matches_of_3 = Match.objects.filter(comp_level__exact='f', match_number__exact=3)
        count = Counter()
        for match in matches_of_3:
            if match.winner is None:
                continue
            for team in match.winner.teams.all():
                count[team] += 1
        matches_of_2 = [x for x in Match.objects.filter(comp_level__exact='f', match_number__exact=2) if
                        not event_has_f3_match(x.event.key)]
        for match in matches_of_2:
            if match.winner is None:
                continue
            for team in match.winner.teams.all():
                count[team] += 1

        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    def highest_win_rate(n=None):
        matches = Match.objects.all()
        wins = Counter()
        total = Counter()
        for match in matches:
            for alliance in match.alliances.all():
                for team in alliance.teams.all():
                    total[team] += 1

            if match.winner is None:
                continue

            for team in match.winner.teams.all():
                wins[team] += 1

        for key, value in total.most_common():
            total[key] = wins[key] / total[key]

        return total.most_common() if n is None else total.most_common(n)


class EventLeaderboard:
    @staticmethod
    def highest_match_average_score(n=None):
        events = Event.objects.all()
        ranks = {}
        for event in events:
            ranks[event] = event.get_average_overall_match_score()

        # todo: add n
        return sorted(ranks.items(), key=itemgetter(1))

    @staticmethod
    # todo: change to get_average_stuff_score()
    def highest_playoff_match_average_score(n=None):
        events = Event.objects.all()
        count = Counter()
        for event in events:
            matches = event.match_set.filter(comp_level__in=['f', 'sf', 'qf', 'ef'])
            if len(matches) == 0:
                continue  # week0 sux
            for match in matches:
                count[event] += match.scoring_model.red_total_score + match.scoring_model.blue_total_score

            count[event] /= len(matches)

        return count.most_common() if n is None else count.most_common(n)

    @staticmethod
    # todo: change to get_average_stuff_score()
    def highest_qual_match_average_score(n=None):
        events = Event.objects.all()
        count = Counter()
        for event in events:
            matches = event.match_set.filter(comp_level__exact='qm')
            if len(matches) == 0:
                continue  # einstein sux
            for match in matches:
                count[event] += match.scoring_model.red_total_score + match.scoring_model.blue_total_score

            count[event] /= len(matches)

        return count.most_common() if n is None else count.most_common(n)
