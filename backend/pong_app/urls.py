# pong_app/urls.py


from django.urls import path
from . import views

app_name = 'pong_app'

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('game/', views.game, name='game'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path('profile/', views.profile, name='profile'),
]

