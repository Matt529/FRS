from django.shortcuts import render

from leaderboard2.models import Leaderboard


def leaderboard_overview(request):
    leaderboards = Leaderboard.objects.all()

    return render(request, 'leaderboard2/overview.html', context={'leaderboards': leaderboards})


def leaderboard(request, field):
    lb = Leaderboard.objects.filter(field__contains=field).first()
    return render(request, 'leaderboard2/leaderboard_spec.html', context={'leaderboard': lb})
