def average_match_score(query_set):
    total = 0
    for match in query_set:
        total += match.scoring_model.blue_total_score + match.scoring_model.red_total_score

    return total / len(query_set)
