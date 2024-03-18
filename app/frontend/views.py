# In your app's views.py file

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from database.models import User
from faker import Faker
import json
import random


@csrf_exempt
def signUp(request):
    # this function will serve two endpoints:
    # 1. When someone wants to access the sign up page (get request)
    # 2. other when someone wants to submit the sign up form

    User = get_user_model()  # if we were using the in built user model then we could access it directly but now we need this method, which comes really handy to get a reference to the current user model being used

    # Logged-in user do not need to register a new account
    if request.user.is_authenticated:
        # replace the below line with where you want your user to be redirected if they are already logged in
        return render(request=request, template_name="home.html")

    # handle the form submission logic here
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password1', '')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            # redirect the user to the home page
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # login the user so they do not have to re enter the same information again
            return redirect("/")
        except Exception:
            messages.error(request, 'Failed to create user: User or Email already exists')
            return render(request=request, template_name="signUp.html", context={})

    # if we receive a get request
    return render(request=request, template_name="signUp.html", context={})


@csrf_exempt
def signIn(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, 'Sign in failed. Please check your Intraname and password.')
            return render(request=request, template_name="signIn.html", context={})
    return render(request=request, template_name="signIn.html", context={})


@csrf_exempt
def update_game_result_pong(request):
    print("UPDATING")
    if request.method == 'POST':
        # Parse JSON data from the request body
        data = json.loads(request.body)
        winner = data.get('winner')
        # Update the logged-in user's data based on the game result
        if winner == request.user.username:
            # Increment the logged-in user's games won count
            request.user.pong_games_won += 1
            request.user.pong_win_streak += 1
            request.user.pong_games_played += 1  # Increment games played
            request.user.save()
            return JsonResponse({'message': 'Game result updated successfully'})
        else:
            request.user.pong_win_streak = 0
            request.user.pong_games_played += 1  # Increment games played
            request.user.save()
            return JsonResponse({'message': 'Game result updated successfully'})
    else:
        # Return error response for unsupported methods
        return JsonResponse({'error': 'Unsupported method'}, status=405)


@csrf_exempt
def update_game_result_memory(request):
    print("UPDATING")
    if request.method == 'POST':
        # Parse JSON data from the request body
        data = json.loads(request.body)
        winner = data.get('winner')
        # Update the logged-in user's data based on the game result
        if winner == request.user.username:
            # Increment the logged-in user's games won count
            request.user.memory_games_won += 1
            request.user.memory_win_streak += 1
            request.user.memory_games_played += 1  # Increment games played
            request.user.save()
            return JsonResponse({'message': 'Game result updated successfully'})
        else:
            request.user.memory_win_streak = 0
            request.user.memory_games_played += 1  # Increment games played
            request.user.save()
            return JsonResponse({'message': 'Game result updated successfully'})
    else:
        # Return error response for unsupported methods
        return JsonResponse({'error': 'Unsupported method'}, status=405)


@csrf_exempt
def get_user_statistics(request):
    if request.user.is_authenticated:
        # Fetch the user's statistics from the database
        user_statistics = {
            'username': request.user.username,
            'pong_games_played': request.user.pong_games_played,
            'pong_games_won': request.user.pong_games_won,
            'pong_win_streak': request.user.pong_win_streak,
            'date_joined': request.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse(user_statistics)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)


@csrf_exempt
def signOut(request):
    if request.user.is_authenticated:
        logout(request)
        messages.error(request, 'Logout successful')
        return render(request=request, template_name="signIn.html", context={})
        # return HttpResponse("<strong>logout successful.<a href='signIn'> Go to Login page</a></strong>")
    else:
        return HttpResponse("<strong>invalid request</strong>")


@csrf_exempt
def editProfile(request):
    User = get_user_model()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if request.method == 'POST':
            if request.POST.get('name') != "":
                user.name = request.POST.get('name')
            if request.POST.get('surname') != "":
                user.surname = request.POST.get('surname')
            if request.POST.get('email') != "":
                user.email = request.POST.get('email')
            # if request.POST.get('birthdate') != "":
            #     user.birthdate = request.POST.get('birthdate')
            user.save()
            # return HttpResponse("Profile updated successfully")
            return render(request=request, template_name="profile.html", context={"user": user})
        return render(request=request, template_name="editProfile.html", context={"user": user})
    else:
        return HttpResponse("You are not logged in")


@csrf_exempt
def showProfile(request):
    User = get_user_model()
    if request.user.is_authenticated:
        # user = User.objects.get(username=request.user.username)
        user = User.objects.get(username=request.user)
        return render(request=request, template_name="profile.html", context={"user": user})


@csrf_exempt
def add_users(request):
    User = get_user_model()
    fake = Faker()

    # Generate 50 users with random data
    users_data = []
    for _ in range(50):
        user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "pong_games_played": random.randint(0, 50),
            "pong_games_won": random.randint(0, 50),
            "pong_win_streak": random.randint(0, 20),
            "pong_tournaments_won": random.randint(0, 5),
            "memory_games_played": random.randint(0, 50),
            "memory_games_won": random.randint(0, 50),
            "memory_win_streak": random.randint(0, 20),
            "memory_tournaments_won": random.randint(0, 5),
            "date_of_creation": fake.date_time_this_decade().isoformat()
        }
        users_data.append(user_data)

    # Loop through the users data and add them to the database if they don't exist
    for user_data in users_data:
        username = user_data['username']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(**user_data)


@csrf_exempt
def showHome(request):
    # Call the function to add users
    return render(request=request, template_name="home.html", context={})


@csrf_exempt
def scoreboard(request):
    User = get_user_model()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        return render(request=request, template_name="scoreboard.html", context={"user": user})


@csrf_exempt
def get_username(request):
    if request.method == 'GET':
        # Assuming the user is authenticated and you want to get the username of the authenticated user
        username = request.user.username
        return JsonResponse({'username': username})


@csrf_exempt
def home(request):
    # Retrieve the top three users based on games won
    top_three_users = User.objects.order_by('-pong_games_won')[:3]
    context = {'top_three_users': top_three_users}
    add_users(request)
    return render(request, 'home.html', context)


@csrf_exempt
def gamePong(request):
    # User = get_user_model()
    # if request.user.is_authenticated:
    #     # user = User.objects.get(username=request.user.username)
    #     user = User.objects.get(username=request.user)
    return render(request, 'gamePong.html', context={})
    # return render(request=request, template_name="pong.html", context={})


@csrf_exempt
def gameMemory(request):
    return render(request, 'gameMemory.html', context={})
