# In your app's views.py file
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import requests
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.timezone import now
import os
from database.models import User
from database.models import Game
from database.models import Tournament
from faker import Faker
import random
from django.utils.translation import gettext, activate, get_language
from django.utils import translation
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from itertools import groupby


def signUp(request):
    User = get_user_model()

    if request.user.is_authenticated:
        return render(request=request, template_name="home.html")

    if request.method == 'POST':
        username = request.POST.get('username', '')
        display_name = request.POST.get('username', '')
        display_name = display_name.replace('-', '')
        print("at signuo: " + display_name)
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1 != password2 or password1 == '' or password2 == '':
            messages.error(request, 'Passwords do not match')
            return render(request=request, template_name="signUp.html", context={})
        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, e.messages)
            return render(request=request, template_name="signUp.html", context={})
        try:
            user = User.objects.create_user(username=username, email=email, password=password1, display_name=display_name)
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                request.user.online = True
                request.user.save()
            return redirect("/")
        except Exception:
            message = gettext('Failed to create user: User or Email already exists')
            messages.error(request, message)
            return render(request=request, template_name="signUp.html", context={})
    return render(request=request, template_name="signUp.html", context={})
# def signUp(request):
#     User = get_user_model()
#     ph = PasswordHasher()

#     if request.user.is_authenticated:
#         return render(request=request, template_name="home.html")

#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         display_name = request.POST.get('username', '')
#         email = request.POST.get('email', '')
#         password1 = request.POST.get('password1', '')
#         password2 = request.POST.get('password2', '')
#         if password1 != password2 or password1 == '' or password2 == '':
#             messages.error(request, 'Passwords do not match')
#             return render(request=request, template_name="signUp.html", context={})
#         try:
#             validate_password(password1)
#         except ValidationError as e:
#             messages.error(request, e.messages)
#             return render(request=request, template_name="signUp.html", context={})
#         try:
#             hashed_password = ph.hash(password1)
#             user = User.objects.create_user(username=username, email=email, password=hashed_password, display_name=display_name)
#             user = authenticate(username=username, password=password1)
#             if user is not None:
#                 login(request, user)
#                 request.user.online = True
#                 request.user.save()
#             return redirect("/")
#         except Exception:
#             messages.error(request, 'Failed to create user: User or Email already exists')
#             return render(request=request, template_name="signUp.html", context={})
#     return render(request=request, template_name="signUp.html", context={})


# def twoFactorAuth()

def signIn(request):
    # User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            print(request.user.display_name)
            login(request, user)
            request.user.online = True
            request.session['user_language'] = user.language
            translation.override(user.language)
            translation.activate(user.language)
            response = HttpResponseRedirect("/")
            user_language = user.language
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
            user.save()
            request.user.save()

            return response
            # return redirect("/")

        else:
            message = gettext('Sign in failed. Please check your Intraname and password.')
            messages.error(request, message)
            return render(request=request, template_name="signIn.html", context={})
    return render(request=request, template_name="signIn.html", context={})


@require_POST
def update_game_result_pong(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        players = data.get('players', [])
        participants = []

        for player in players:
            user = User.objects.filter(display_name=player).first()
            if user:
                participants.append(user)
            else:
                username = player + '_guest'
                display_name = player + '_guest'
                email = player + '@guest.com'
                user = User.objects.filter(display_name=display_name).first()
                if user:
                    participants.append(user)
                else:
                    user = User.objects.create_user(username=username, display_name=display_name, email=email)
                    participants.append(user)

        winner_user = None
        winner = User.objects.filter(display_name=data.get('winner')).first()
        if winner:
            winner_user = winner
        else:
            username = data.get('winner') + '_guest'
            display_name = data.get('winner') + '_guest'
            email = data.get('winner') + '@guest.com'
            user = User.objects.filter(display_name=display_name).first()
            if user:
                winner_user = user
            else:
                winner_user = User.objects.create_user(username=username, display_name=display_name, email=email)

        tournamentObj = None
        is_tournament_bool = data.get('is_tournament')
        if is_tournament_bool:
            tournament_id = data.get('tournament_id')
            if tournament_id:
                # If tournament ID is provided, retrieve the tournament object
                try:
                    tournamentObj = Tournament.objects.get(pk=tournament_id)
                except Tournament.DoesNotExist:
                    pass
            else:
                pass

        # Create the Pong game object
        pong_id = Game.objects.create(
            is_tournament=data.get('is_tournament'),
            pong_game=True,
            scoreToDo=data.get('scoreToDo'),
            score_winner=data.get('scoreW'),
            score_loser=data.get('scoreL'),
            game_date=now(),
            winner=winner_user,
            tournament=tournamentObj
        )
        pong_id.participants.add(*participants)
        pong_id.save()

        return JsonResponse({'message': 'Game result updated successfully'})
    else:
        # Return error response for unsupported methods
        return JsonResponse({'error': 'Unsupported method'}, status=405)


@require_POST
def start_tournament(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_date = datetime.now()
        participants_data = data.get('participants', [])

        # Create the tournament object
        tournament = Tournament.objects.create(
            start_date=start_date,
            number_of_participants=len(participants_data),
            pong_tournament=data.get('pong_tournament'),
            memory_tournament=data.get('memory_tournament')
            # Set other fields as needed
        )
        tournament.participants.set(participants_data)
        response_data = {
            'message': 'Tournament started successfully',
            'tournament_id': tournament.tournament_id
        }
        return JsonResponse(response_data)
    else:
        # Return error response for unsupported methods
        return JsonResponse({'error': 'Unsupported method'}, status=405)


def end_tournament(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        end_date = timezone.now()
        tournament_id = data.get('tournament_id')
        winner = data.get('winner')

        winner_user = None
        winner = User.objects.filter(display_name=data.get('winner')).first()
        if winner:
            winner_user = winner
        else:
            username = data.get('winner') + '_guest'
            display_name = data.get('winner') + '_guest'
            email = data.get('winner') + '@guest.com'
            user = User.objects.filter(display_name=display_name).first()
            if user:
                winner_user = winner
            else:
                winner_user = User.objects.create_user(username=username, display_name=display_name, email=email)

        if tournament_id:
            # If tournament ID is provided, retrieve the tournament object
            try:
                tournamentObj = Tournament.objects.get(pk=tournament_id)
            except Tournament.DoesNotExist:
                return JsonResponse({'error': 'Tournament does not exist'}, status=404)
            tournamentObj.end_date = end_date
            tournamentObj.winner = winner_user
            tournamentObj.save()
            return JsonResponse({'message': 'Tournament result updated successfully'})
        else:
            return JsonResponse({'error': 'Unsupported method'}, status=405)


def update_game_result_memory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        players = data.get('players', [])
        participants = []
        for player in players:
            user = User.objects.filter(display_name=player).first()
            if user:
                participants.append(user)
            else:
                username = player + '_guest'
                display_name = player + '_guest'
                email = player + '@guest.com'
                user = User.objects.filter(display_name=display_name).first()
                if user:
                    participants.append(user)
                else:
                    user = User.objects.create_user(username=username, display_name=display_name, email=email)

        tournamentObj = None
        is_tournament = data.get('tournament')
        if is_tournament:
            tournament_id = data.get('tournament_id')
            if tournament_id:
                # If tournament ID is provided, retrieve the tournament object
                try:
                    tournamentObj = Tournament.objects.get(pk=tournament_id)
                except Tournament.DoesNotExist:
                    # Handle the case where the provided tournament ID does not exist
                    # You may raise an error, return an appropriate response, or handle it as needed
                    pass
            else:
                # If tournament ID is not provided, create a new tournament
                start_date = datetime.now()
                # You need to get participants from data or provide it from somewhere
                participants = data.get('participants', [])
                tournamentObj = Tournament.objects.create(
                    start_date=start_date,
                    number_of_participants=len(participants),
                    # Set other fields as needed
                )
        # Create the Pong game object
        memory_id = Game.objects.create(
            is_tournament=data.get('tournament'),
            memory_game=True,
            chosen_set=data.get('chosenSet'),
            number_of_cards=data.get('numberOfCards'),
            score_winner=data.get('scoreW'),
            score_loser=data.get('scoreL'),
            game_date=now(),
            winner=User.objects.filter(display_name=data.get('winner')).first(),
            tournament=tournamentObj
        )
        memory_id.participants.add(*participants)
        memory_id.save()

        return JsonResponse({'message': 'Game result updated successfully'})
    else:
        # Return error response for unsupported methods
        return JsonResponse({'error': 'Unsupported method'}, status=405)


def start_tournament_memory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tournament_name = data.get('tournament_name')
        start_date = datetime.now()

        # Create the tournament object
        tournament = Tournament.objects.create(
            tournament_name=tournament_name,
            start_date=start_date,
            number_of_participants=data.get('number_of_participants'),
            pong_tournament=True
            # Set other fields as needed
        )
        response_data = {
            'message': 'Tournament started successfully',
            'tournament_id': tournament.tournament_id
        }
        return JsonResponse(response_data)
    else:
        # Return error response for unsupported methods
        return JsonResponse({'error': 'Unsupported method'}, status=405)


def get_user_statistics(request):
    if request.user.is_authenticated:
        # Fetch the user's statistics from the database
        user_statistics = {
            'username': request.user.username,
            'date_joined': request.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        }

        # Fetch all games associated with the user
        user_games = Game.objects.filter(participants=request.user)
        games_data = []
        for game in user_games:
            games_data.append({
                'game_date': game.game_date.strftime('%Y-%m-%d %H:%M:%S'),
                'pong_game': game.pong_game,
                'memory_game': game.memory_game,
                'is_tournament': game.is_tournament,
                'winner': game.winner.username,
                'score_winner': game.score_winner,
                'score_loser': game.score_loser,
                'tournament_id': game.tournament_id,
                'participants': [participant.username for participant in game.participants.all()]
                # Add more fields as needed
            })

        # Combine user statistics and games data
        user_data = {
            'user_statistics': user_statistics,
            'games_data': games_data,
        }

        return JsonResponse(user_data)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)


def signOut(request):
    if request.user.is_authenticated:
        request.user.online = False
        request.user.save()
        logout(request)
        # Create a response
        response = HttpResponseRedirect('/')
        # Clear the language cookie
        response.delete_cookie(settings.LANGUAGE_COOKIE_NAME)
        message = gettext('Logout successful')
        messages.error(request, message)
        return render(request=request, template_name="signIn.html", context={})
        # return HttpResponse("<strong>logout successful.<a href='signIn'> Go to Login page</a></strong>")
    else:
        message = gettext('Something went wrong! Are you signed in?')
        messages.error(request, message)
        return render(request=request, template_name="signIn.html", context={})


def editProfile(request):
    User = get_user_model()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if request.method == 'POST':
            if request.POST.get('name') != "":
                user.name = request.POST.get('name')
            if request.POST.get('displayName') != "":
                user.display_name = request.POST.get('displayName')
            if request.POST.get('surname') != "":
                user.surname = request.POST.get('surname')
            if request.POST.get('email') != "":
                user.email = request.POST.get('email')
            if request.POST.get('language') != "":
                user.language = request.POST.get('language')
                request.session['user_language'] = user.language
                user.save()
                request.session['user_language'] = user.language
                translation.override(user.language)
                translation.activate(user.language)
                response = HttpResponseRedirect("/")
                user_language = user.language
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
                request.user.save()

            user.save()
            return response
        return render(request=request, template_name="editProfile.html", context={"user": user})
    else:
        message = gettext('You are not signed in! Please sign in to edit your profile.')
        messages.error(request, message)
        return render(request=request, template_name="signIn.html", context={})


def showProfile(request):
    User = get_user_model()
    if request.user.is_authenticated:
        # user = User.objects.get(username=request.user.username)
        user = User.objects.get(username=request.user)
        return render(request=request, template_name="profile.html", context={"user": user, "timestamp": now()})
    else:
        message = gettext('You are not signed in! Please sign in to view your profile.')
        messages.error(request, message)
        return render(request=request, template_name="signIn.html", context={})


def add_users(request):
    User = get_user_model()
    fake = Faker()

    # Generate 50 users with random data
    users_data = []
    for _ in range(3):
        user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "display_name": fake.user_name(),
            "date_of_creation": fake.date_time_this_decade().isoformat()
        }
        users_data.append(user_data)

    # Loop through the users data and add them to the database if they don't exist
    for user_data in users_data:
        username = user_data['username']
        email = user_data['email']
        display_name = user_data['display_name']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if not User.objects.filter(display_name=display_name).exists():
                    User.objects.create_user(**user_data)


def showHome(request):
    if request.user.is_authenticated:
        return render(request=request, template_name="home.html", context={})
    else:
        message = gettext('You are not signed in! Please sign in to view the home page.')
        messages.error(request, message)
        return render(request=request, template_name="signIn.html", context={})


def showChat(request):
    return render(request, 'chat.html')


def scoreboard(request):
    User = get_user_model()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        pong_games = Game.objects.filter(participants=user, pong_game=True).order_by('game_date')
        memory_games = Game.objects.filter(participants=user, memory_game=True).order_by('game_date')
        games_played = Game.objects.filter(participants=user).order_by('-game_date')
        # Calculate win streak for pong game
        pong_max_win_streak = calculate_win_streak(pong_games, user)

        # Calculate win streak for memory game
        memory_max_win_streak = calculate_win_streak(memory_games, user)

        # Count games played and won for both pong and memory games
        games_played_pong = pong_games.count()
        games_won_pong = Game.objects.filter(winner=user, pong_game=True).count()
        games_played_memory = memory_games.count()
        games_won_memory = Game.objects.filter(winner=user, memory_game=True).count()

        context = {
            'games_played_pong': games_played_pong,
            'games_won_pong': games_won_pong,
            'games_played_memory': games_played_memory,
            'games_won_memory': games_won_memory,
            'pong_max_win_streak': pong_max_win_streak,
            'memory_max_win_streak': memory_max_win_streak,
            'all_games': games_played
        }
        return render(request, 'scoreboard.html', context)
    else:
        messages.error(request, 'You are not signed in! Please sign in to view the scoreboard.')
        return render(request=request, template_name="signIn.html", context={})


def calculate_win_streak(games, user):
    win_streak = 0
    max_win_streak = 0
    for game in games:
        if game.winner == user:
            win_streak += 1
            max_win_streak = max(max_win_streak, win_streak)
        else:
            win_streak = 0
    return max_win_streak


def get_display_name(request):
    if request.method == 'GET':
        # Assuming the user is authenticated and you want to get the username of the authenticated user
        display_name = request.user.display_name
        return JsonResponse({'display_name': display_name})


def home(request):
    # Retrieve the top three users based on games won
    # top_three_users = User.objects.order_by('-pong_games_won')[:3]
    top_three_users = User.objects.order_by('username')[:3]

    context = {'top_three_users': top_three_users}
    add_users(request)
    return render(request, 'home.html', context)


def gamePong(request):
    # User = get_user_model()
    if request.user.is_authenticated:
        return render(request, 'gamePong.html', context={})
    else:
        message = gettext('You are not signed in! Please sign in to play the game.')
        messages.error(request, message)
        return render(request=request, template_name="signIn.html", context={})


def callback(request):
    User = get_user_model()

    code = request.GET.get('code')
    if code:
        data = {
            'grant_type': 'authorization_code',
            'client_id': os.environ.get("OAUTH_CLIENT_ID"),
            'client_secret': os.environ.get("OAUTH_CLIENT_SECRET"),
            'code': code,
            'redirect_uri': os.environ.get("OAUTH_CALLBACK_URL"),
            # 'redirect_uri': 'https://42pong.ddns.net:9999/callback'
        }

        try:
            response = requests.post('https://api.intra.42.fr/oauth/token', data=data)
            response_data = response.json()
            access_token = response_data['access_token']

            user_info_response = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': f'Bearer {access_token}'})
            user_info = user_info_response.json()
            # print(user_info)
            username = user_info['login']
            email = user_info['email']
            avatar_url = user_info['image']['link']
            surename = user_info['last_name']
            name = user_info['first_name']
            password1 = user_info['login'] + "@secretpw1#"
            display_name = user_info['login']
            display_name = display_name.replace('-', '')
            user = User.objects.filter(username=username).first()
            if user:
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    user.online = True
                    request.session['user_language'] = user.language
                    translation.override(user.language)
                    translation.activate(user.language)
                    response = HttpResponseRedirect("/")
                    user_language = user.language
                    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
                    request.user.save()
                    user.save()
                return (response)
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, avatar_url=avatar_url, name=name, surname=surename, display_name=display_name)

                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    user.online = True
                    user.save()
                return redirect("/")

        except Exception:
            message = gettext('Failed to authenticate user. Please try again.')
            messages.error(request, message)
            return render(request=request, template_name="signIn.html", context={})
    else:
        message = gettext('Failed to reach API. Please try again.')
        messages.error(request, message)
        return render(request=request, template_name="signIn.html", context={})


def changeAvatar(request):
    User = get_user_model()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.method == 'POST':
            avatar_url = request.POST.get('avatar_url', '').strip()
            uploaded_file = request.FILES.get('avatar_file')
            selected_avatar = request.POST.get('static_avatar')

            if avatar_url:
                user.avatar_url = avatar_url
            elif uploaded_file:
                fs = FileSystemStorage()
                file_name = fs.save(uploaded_file.name, uploaded_file)
                uploaded_file_url = fs.url(file_name)
                protocol = 'https' if request.is_secure() else 'http'
                host = request.get_host()
                if ':' not in host:
                    port = '9999'
                    host_with_port = f"{host}:{port}"
                else:
                    host_with_port = host
                user.avatar_url = f"{protocol}://{host_with_port}{uploaded_file_url}"
            elif selected_avatar:
                robot_avatars_path = os.path.join(settings.STATIC_ROOT, 'img', 'Robot')
                if selected_avatar in os.listdir(robot_avatars_path):
                    user.avatar_url = os.path.join(settings.STATIC_URL, 'img', 'Robot', selected_avatar)

            user.last_modified = now()
            user.save()
            return render(request=request, template_name="profile.html", context={"user": user})
        else:
            robot_avatars_path = os.path.join(settings.STATIC_ROOT, 'img', 'Robot')
            robot_avatars_url = os.path.join(settings.STATIC_URL, 'img', 'Robot')
            available_avatars = [(file, os.path.join(robot_avatars_url, file))
                                 for file in os.listdir(robot_avatars_path)
                                 if os.path.isfile(os.path.join(robot_avatars_path, file)) and file.endswith('.png')] if os.path.isdir(robot_avatars_path) else []
            return render(request, 'changeAvatar.html', {'user': user, 'available_avatars': available_avatars})
    else:
        message = gettext('You are not signed in! Please sign in to edit your profile.')
        messages.error(request, message)
        return redirect('signIn')


def searchUsers(request):
    User = get_user_model()
    if request.user.is_authenticated:
        if request.method == "GET":
            username = request.GET.get('username', None)
            if username:
                try:
                    user = User.objects.get(username=username)
                    # Adjusted to match your User model fields
                    return JsonResponse({"username": user.username, "user_id": user.pk, "online": user.online}, safe=False)
                except User.DoesNotExist:
                    return JsonResponse({"error": "User not found"}, status=404)
            return JsonResponse({"error": "No username provided"}, status=400)
    else:
        return JsonResponse({"error": "Unauthorized access"}, status=401)


@login_required
def addFriend(request):
    User = get_user_model()
    if request.method == 'POST':
        data = json.loads(request.body)
        friend_username = data.get('username_', '').strip()

        if not friend_username:
            return JsonResponse({"error": "Username required."}, status=400)

        if friend_username == request.user.username:
            return JsonResponse({"error": "You cannot add yourself as a friend."}, status=400)

        try:
            friend = User.objects.get(username=friend_username)
            request.user.friends.add(friend)  # Using ManyToManyField's add() method
            return JsonResponse({"success": True, "message": "Friend added successfully.", "friend_username": friend_username, "online": friend.online})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
    #     try:
    #         friend = User.objects.get(username=friend_username)
    #     except User.DoesNotExist:
    #         return JsonResponse({"error": "User not found."}, status=404)

    #     current_friends = request.user.friends
    #     if friend.pk in current_friends:
    #         return JsonResponse({"error": "This user is already your friend."}, status=400)

    #     current_friends.append(friend.pk)
    #     request.user.friends = current_friends
    #     request.user.save()

    #     return JsonResponse({"success": True, "message": "Friend added successfully.", "friend_username": friend_username, "online": friend.online})
    # else:
    #     return JsonResponse({"error": "Invalid request method."}, status=405)


def showFriends(request):
    # User = get_user_model()
    if request.user.is_authenticated:
        # friend_ids = request.user.friends
        # friends = User.objects.filter(pk__in=friend_ids)
        friends = request.user.friends.all()
        return render(request, 'showFriends.html', {'friends': friends})
    else:
        messages.error(request, 'You are not signed in! Please sign in to view your friends.')
        return render(request=request, template_name="signIn.html", context={})


@login_required
def removeFriends(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        friend_ids_to_remove = data.get('friend_ids', [])

        for friend_id in friend_ids_to_remove:
            try:
                friend = User.objects.get(user_id=friend_id)
                request.user.friends.remove(friend)  # Using ManyToManyField's remove() method
            except User.DoesNotExist:
                pass  # Handle error or ignore if friend not found

        return JsonResponse({"success": True, "message": "Selected friends removed successfully."})

    #     current_friends = request.user.friends

    #     request.user.friends = [friend_id for friend_id in current_friends if str(friend_id) not in friend_ids_to_remove]
    #     request.user.save()

    #     return JsonResponse({"success": True, "message": "Selected friends removed successfully."})
    # else:
    #     return JsonResponse({"error": "Invalid request method"}, status=405)


def gameMemory(request):
    if request.user.is_authenticated:
        return render(request, 'gameMemory.html', context={})
    else:
        messages.error(request, 'You are not signed in! Please sign in to play the game.')
        return render(request=request, template_name="signIn.html", context={})
