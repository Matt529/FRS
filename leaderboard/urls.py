from django.conf.urls import url

urlpatterns = [
    url(r'^leaderboard/$', 'leaderboard.views.elo_leaders')
]
