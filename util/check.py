from TBAW.models import Team


def team_exists(team_number):
    return Team.objects.filter(team_number=team_number).exists()
