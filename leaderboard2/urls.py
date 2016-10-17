from django.conf.urls import url

from leaderboard2 import views

urlpatterns = [
    url(r'^$', views.leaderboard_overview, name='leaderboard_overview'),
    url(r'^(?P<category>(a|A)ll|[0-9]{4})/$', views.category_overview, name='category_overview'),
    url(r'^(?P<field>.*)/$', views.leaderboard, name='leaderboard_spec'),
]
