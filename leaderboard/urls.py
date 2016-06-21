from django.conf.urls import url
from .views import leaderboard

urlpatterns = [
    url(r'^leaderboard/$', leaderboard, name='leaderboard'),
]
