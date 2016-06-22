from django.conf.urls import url
from leaderboard import views

urlpatterns = [
    url(r'^leaderboard/$', views.elo_leaders, name='elo_leaders')
]
