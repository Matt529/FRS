from TBAW.models import Match
from collections import Counter


class AllianceLeaderboard:
    @staticmethod
    def most_wins():
        matches = Match.objects.all()
        count = Counter()
        for m in matches:
            count[m.winner] += 1
        # Remove ties
        del count[None]
        return count.most_common(5)


class TeamLeaderboard:
    @staticmethod
    def most_wins():
        matches = Match.objects.all()
        count = Counter()
        for m in matches:
            if m.winner is None:
                continue
            for team in m.winner.teams.all():
                count[team] += 1
        return count.most_common(5)
