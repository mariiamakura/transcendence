# In your app's views.py file

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
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


def signUp(request):
    User = get_user_model()

    if request.user.is_authenticated:
        return render(request=request, template_name="home.html")

    if request.method == 'POST':
        username = request.POST.get('username', '')
        display_name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
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
            messages.error(request, 'Failed to create user: User or Email already exists')
            return render(request=request, template_name="signUp.html", context={})
    return render(request=request, template_name="signUp.html", context={})


def signIn(request):
    # User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.user.online = True
            request.user.save()

            # user_ = User.objects.get(username=request.user)
            # user_.online = True
            # user_.save()

            return redirect("/")
        else:
            messages.error(request, 'Sign in failed. Please check your Intraname and password.')
            return render(request=request, template_name="signIn.html", context={})
    return render(request=request, template_name="signIn.html", context={})


def home(request):
    return render(request=request, template_name="home.html", context={})


def signOut(request):
    if request.user.is_authenticated:
        request.user.online = False
        request.user.save()
        logout(request)
        messages.error(request, 'Logout successful')
        return render(request=request, template_name="signIn.html", context={})
        # return HttpResponse("<strong>logout successful.<a href='signIn'> Go to Login page</a></strong>")
    else:
        messages.error(request, 'Something went wrong! Are you signed in?')
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
            if request.POST.get('birthdate') != "":
                user.birthdate = request.POST.get('birthdate')
            # if request.POST.get('avatar_url') != "":
            #     user.avatar_url = request.POST.get('avatar_url')
            user.save()
            # return HttpResponse("Profile updated successfully")
            return render(request=request, template_name="profile.html", context={"user": user})
        return render(request=request, template_name="editProfile.html", context={"user": user})
    else:
        messages.error(request, 'You are not signed in! Please sign in to edit your profile.')
        return render(request=request, template_name="signIn.html", context={})


def showProfile(request):
    User = get_user_model()
    if request.user.is_authenticated:
        # user = User.objects.get(username=request.user.username)
        user = User.objects.get(username=request.user)
        return render(request=request, template_name="profile.html", context={"user": user, "timestamp": now()})
    else:
        messages.error(request, 'You are not signed in! Please sign in to view your profile.')
        return render(request=request, template_name="signIn.html", context={})


def showHome(request):
    if request.user.is_authenticated:
        return render(request=request, template_name="home.html", context={})
    else:
        messages.error(request, 'You are not signed in! Please sign in to view the home page.')
        return render(request=request, template_name="signIn.html", context={})


def showChat(request):
    return render(request, 'chat.html')


def gamePong(request):
    # User = get_user_model()
    if request.user.is_authenticated:
        return render(request, 'gamePong.html', context={})
    else:
        messages.error(request, 'You are not signed in! Please sign in to play the game.')
        return render(request=request, template_name="signIn.html", context={})


def callback(request):
    User = get_user_model()

    code = request.GET.get('code')
    if code:
        data = {
            'grant_type': 'authorization_code',
            # 'client_id': 'u-s4t2ud-ff92aa7c60b93ab9ab76619c369de4f8c7bb33c3e8c8a0ffdb386d35d2007a4c',
            # 'client_secret': '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',
            'client_id': os.environ.get("OAUTH_CLIENT_ID"),
            'client_secret': os.environ.get("OAUTH_CLIENT_SECRET"),
            'code': code,
            'redirect_uri': 'https://localhost:9999/callback'
        }

        try:
            response = requests.post('https://api.intra.42.fr/oauth/token', data=data)
            response_data = response.json()
            access_token = response_data['access_token']

            user_info_response = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': f'Bearer {access_token}'})
            user_info = user_info_response.json()
            print(user_info)

            username = user_info['login']
            password1 = user_info['login']
            email = user_info['email']
            avatar_url = user_info['image']['link']
            surename = user_info['last_name']
            name = user_info['first_name']
            display_name = user_info['login']
            # # campus = user_info['campus']
            # # level = user_info['cursus_users'][0]['level']

            user = User.objects.filter(username=username).first()
            if user:
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    user.online = True
                    user.save()
                return redirect("/")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, avatar_url=avatar_url, name=name, surname=surename, display_name=display_name)

                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    user.online = True
                    user.save()
                return redirect("/")

        except Exception:
            messages.error(request, 'Failed to authenticate user. Please try again.')
            return render(request=request, template_name="signIn.html", context={})
    else:
        messages.error(request, 'Failed to reach API. Please try again.')
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
        messages.error(request, 'You are not signed in! Please sign in to edit your profile.')
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
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        current_friends = request.user.friends
        if friend.pk in current_friends:
            return JsonResponse({"error": "This user is already your friend."}, status=400)

        current_friends.append(friend.pk)
        request.user.friends = current_friends
        request.user.save()

        return JsonResponse({"success": True, "message": "Friend added successfully.", "friend_username": friend_username, "online": friend.online})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def showFriends(request):
    User = get_user_model()
    if not request.user.is_authenticated:
        return redirect('signIn')
    friend_ids = request.user.friends
    friends = User.objects.filter(pk__in=friend_ids)

    return render(request, 'showFriends.html', {'friends': friends})


@login_required
def removeFriends(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        friend_ids_to_remove = data.get('friend_ids', [])
        current_friends = request.user.friends

        request.user.friends = [friend_id for friend_id in current_friends if str(friend_id) not in friend_ids_to_remove]
        request.user.save()

        return JsonResponse({"success": True, "message": "Selected friends removed successfully."})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
