from itertools import combinations

from TBAW.models import Match, Alliance, Team, Event, RankingModel
from collections import Counter
from operator import itemgetter
from util.check import event_has_f3_match
from util.generators import non_championship_teams


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
            if total[key] >= 14:
                total[key] = wins[key] / total[key]
            else:
                del total[key]

        return total.most_common() if n is None else total.most_common(n)

    @staticmethod
    def highest_non_champs_win_rate(n=None):
        # highest = highest_team_win_rate(Match.objects.filter(alliances__teams__in=non_championship_teams(2016)))
        # for team in highest:
        #     if team[0].went_to_champs(2016):
        #         del team
        #
        # return highest[:n]

        wins = Counter()
        total = Counter()
        teams = non_championship_teams(2016)
        for team in teams:
            matches = Match.objects.filter(alliances__teams__key=team.key)

            if len(matches) < 10:
                continue

            for match in matches:
                total[team] += 1

                if match.winner is None:
                    continue

                if team in match.winner.teams.all():
                    wins[team] += 1

            if total[team] != 0:
                total[team] = wins[team] / total[team]

        return total.most_common() if n is None else total.most_common(n)


class EventLeaderboard:
    @staticmethod
    def highest_match_average_score(n=None):
        events = Event.objects.all()
        ranks = {}
        for event in events:
            ranks[event] = event.get_average_overall_match_score()

        return sorted(ranks.items(), key=itemgetter(1), reverse=True)[:n]

    @staticmethod
    def highest_playoff_match_average_score(n=None):
        events = Event.objects.all()
        ranks = {}
        for event in events:
            ranks[event] = event.get_average_playoff_match_score()

        return sorted(ranks.items(), key=itemgetter(1), reverse=True)[:n]

    @staticmethod
    def highest_qual_match_average_score(n=None):
        events = Event.objects.exclude(event_code__exact='cmp')  # cmp doesn't have qualifiers
        ranks = {}
        for event in events:
            ranks[event] = event.get_average_qual_match_score()

        return sorted(ranks.items(), key=itemgetter(1), reverse=True)[:n]


class OtherLeaderboard:
    @staticmethod
    def region_highest_average_score(n=None):
        matches = Match.objects.all()
        totals = Counter()
        counts = Counter()
        for match in matches:
            for alliance in match.alliances.all():
                for team in alliance.teams.all():
                    counts['{0}, {1}'.format(team.region, team.country_name)] += 1
                    if alliance.get_color_display() == 'Red':
                        totals['{0}, {1}'.format(team.region, team.country_name)] += \
                            match.scoring_model.red_total_score
                    else:
                        totals['{0}, {1}'.format(team.region, team.country_name)] += \
                            match.scoring_model.blue_total_score

        for key, value in totals.most_common():
            totals[key] = totals[key] / counts[key]

        return totals.most_common() if n is None else totals.most_common(n)
