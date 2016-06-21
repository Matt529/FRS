from django.db.models import F
from django.shortcuts import render
from .models import TeamLeaderboard


def leaderboard(request):
    annotated_queryset = TeamLeaderboard.highest_elo(100).annotate(elo_max=F('elo_mu') + F('elo_sigma'),
                                                                   elo_min=F('elo_mu') - F('elo_sigma'))
    return render(request, 'leaderboard.html',
                  context={
                      'elo_leaders': annotated_queryset
                  })
