from annoying.decorators import render_to

from leaderboard2.models import Leaderboard


@render_to('leaderboard2/overview.html')
def leaderboard_overview(request):
    leaderboards = Leaderboard.objects.all()

    return {'leaderboards': leaderboards}


@render_to('leaderboard2/leaderboard_spec.html')
def leaderboard(request, field):
    lb = Leaderboard.objects.filter(field__contains=field).first()
    return {'leaderboard': lb}
