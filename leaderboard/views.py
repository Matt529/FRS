from django.shortcuts import render
from .models import TeamLeaderboard


def leaderboard(request):
    return render(request, 'TBAW/leaderboard.html',
                  context={
                      'elo_leaders': TeamLeaderboard.highest_elo(100)
                  })
