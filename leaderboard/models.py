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


# not working
class TeamLeaderboard:
    @staticmethod
    def most_wins():
        matches = Match.objects.all()
        count = Counter()
        for m in matches:
            for team in m.winner.objects.all():
                count[team] += 1
        return count.most_common(5)
