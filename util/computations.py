from collections import Counter


def average_match_score(query_set):
    if len(query_set) == 0:
        return 0

    total = 0
    for match in query_set:
        total += match.scoring_model.blue_total_score + match.scoring_model.red_total_score

    return total / len(query_set)


def highest_team_win_rate(query_set):
    if len(query_set) == 0:
        return 0

    wins = Counter()
    total = Counter()
    for match in query_set:
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

    return total.most_common()
