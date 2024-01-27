# pong_app/views.py

from django.shortcuts import render

def welcome(request):
    return render(request, 'pong_app/welcome.html')

def game(request):
    return render(request, 'pong_app/game.html')

def scoreboard(request):
    return render(request, 'pong_app/scoreboard.html')

def profile(request):
    return render(request, 'pong_app/profile.html')
