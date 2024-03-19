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
        display_name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request=request, template_name="signUp.html", context={})
        try:
            user = User.objects.create_user(username=username, email=email, password=password1, display_name=display_name)
            # redirect the user to the home page
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)  # login the user so they do not have to re enter the same information again
            return redirect("/")
        except Exception:
            messages.error(request, 'Failed to create user: User or Email already exists')
            return render(request=request, template_name="signUp.html", context={})

    # if we receive a get request
    return render(request=request, template_name="signUp.html", context={})


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


def home(request):
    return render(request=request, template_name="home.html", context={})


def signOut(request):
    if request.user.is_authenticated:
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
    # return render(request=request, template_name="chat.html", context={})


def gamePong(request):
    # User = get_user_model()
    if request.user.is_authenticated:
        return render(request, 'gamePong.html', context={})
    else:
        messages.error(request, 'You are not signed in! Please sign in to play the game.')
        return render(request=request, template_name="signIn.html", context={})
    # return render(request=request, template_name="pong.html", context={})


def callback(request):
    User = get_user_model()

    code = request.GET.get('code')
    if code:
        data = {
            'grant_type': 'authorization_code',
            'client_id': 'u-s4t2ud-ff92aa7c60b93ab9ab76619c369de4f8c7bb33c3e8c8a0ffdb386d35d2007a4c',
            'client_secret': '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',
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
                    login(request, user)  # login the user so they do not have to re enter the same information again
                return redirect("/")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, avatar_url=avatar_url, name=name, surname=surename, display_name=display_name)
                # redirect the user to the home page
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)  # login the user so they do not have to re enter the same information again
                return redirect("/")

            # Here, use the user_info to authenticate or create a user in your system
            # This step depends on how you manage users in your Django project
            # For example, you could match users by their email or a custom user ID from 42

            # Assuming you have a method to get or create a Django user:
            # user = get_or_create_user(user_info)
            # login(request, user)

            # return redirect('/')  # Redirect to the home page or dashboard
        except Exception:
            # Handle errors, e.g., invalid code, request failure
            messages.error(request, 'Failed to authenticate user. Please try again.')
            return render(request=request, template_name="signIn.html", context={})
    else:
        messages.error(request, 'Failed to reach API. Please try again.')
        return render(request=request, template_name="signIn.html", context={})


def changeAvatar(request):
    User = get_user_model()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)  # Ensure you're using the correct attribute for username
        if request.method == 'POST':
            avatar_url = request.POST.get('avatar_url', '').strip()
            uploaded_file = request.FILES.get('avatar_file')
            selected_avatar = request.POST.get('static_avatar')

            if avatar_url:
                # Handle URL input
                user.avatar_url = avatar_url
            elif uploaded_file:
                # Handle file upload
                fs = FileSystemStorage()  # Use MEDIA_ROOT for storage
                file_name = fs.save(uploaded_file.name, uploaded_file)
                uploaded_file_url = fs.url(file_name)
                # Explicitly build the absolute URI with port number
                protocol = 'https' if request.is_secure() else 'http'
                host = request.get_host()
                if ':' not in host:  # Add port number if not present
                    port = '9999'  # Default to 9999 if not found in request
                    host_with_port = f"{host}:{port}"
                else:
                    host_with_port = host
                user.avatar_url = f"{protocol}://{host_with_port}{uploaded_file_url}"
            elif selected_avatar:
                # Handle static file selection
                robot_avatars_path = os.path.join(settings.STATIC_ROOT, 'img', 'Robot')
                if selected_avatar in os.listdir(robot_avatars_path):
                    user.avatar_url = os.path.join(settings.STATIC_URL, 'img', 'Robot', selected_avatar)

            user.last_modified = now()
            user.save()
            return render(request=request, template_name="profile.html", context={"user": user})
        else:
            # List available .png avatars from static folder with URLs for preview
            robot_avatars_path = os.path.join(settings.STATIC_ROOT, 'img', 'Robot')
            robot_avatars_url = os.path.join(settings.STATIC_URL, 'img', 'Robot')
            available_avatars = [(file, os.path.join(robot_avatars_url, file))
                                 for file in os.listdir(robot_avatars_path)
                                 if os.path.isfile(os.path.join(robot_avatars_path, file)) and file.endswith('.png')] if os.path.isdir(robot_avatars_path) else []
            return render(request, 'changeAvatar.html', {'user': user, 'available_avatars': available_avatars})
    else:
        messages.error(request, 'You are not signed in! Please sign in to edit your profile.')
        return redirect('signIn')


# def showFriends(request):
#     User = get_user_model()
#     if request.user.is_authenticated:
#         user = User.objects.get(username=request.user)

#         friends_ids = user.friends
#         friends = list(User.objects.filter(user_id__in=friends_ids))
#         return render(request=request, template_name="showFriends.html", context={"user": user, "friends": friends})
#     else:
#         messages.error(request, 'You are not signed in! Please sign in to view your friends.')
#         return render(request=request, template_name="signIn.html", context={})


def searchUsers(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            username = request.GET.get('username', None)
            if username:
                User = get_user_model()
                try:
                    user = User.objects.get(username=username)
                    # You might want to return more details or render a template
                    return JsonResponse({"username": user.username, "user_id": user.user_id, "online": user.online}, safe=False)
                except User.DoesNotExist:
                    return JsonResponse({"error": "User not found"}, status=404)
            return JsonResponse({"error": "No username provided"}, status=400)


@login_required
@csrf_exempt
def addFriend(request):
    if request.method == 'POST':
        User = get_user_model()
        data = json.loads(request.body)
        friend_username = data.get('friend_username', '').strip()

        if not friend_username:
            return JsonResponse({"error": "Username required."}, status=400)

        if friend_username == request.user.username:
            return JsonResponse({"error": "You cannot add yourself as a friend."}, status=400)

        try:
            friend = User.objects.get(username=friend_username)
            friend  # to avoid flake warning
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        # Updated check for already a friend
        if any(friend['username'] == friend_username for friend in request.user.friends):
            return JsonResponse({"error": "This user is already your friend."}, status=400)

        request.user.friends.append(friend.pk)  # Add friend

        # request.user.friends.append({"username": friend_username})
        request.user.save()

        return JsonResponse({"success": True, "message": "Friend added successfully.", "friend_username": friend_username})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def showFriends(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not signed in! Please sign in to view your friends.')
        return redirect('signIn')

    # Assuming 'friends' is a list of user IDs stored in a JSONField.
    User = get_user_model()
    friend_ids = request.user.friends
    friends = User.objects.filter(user_id__in=friend_ids)

    return render(request, 'showFriends.html', {'friends': friends})

# def showFriends(request):
#     if not request.user.is_authenticated:
#         messages.error(request, "You need to be signed in to view friends.")
#         return redirect("signIn")

#     friend_ids = request.user.friends  # Assuming this is a list of IDs
#     friends = []

#     for friend_id in friend_ids:
#         try:
#             friend = User.objects.get(id=friend_id)
#             friends.append(friend)
#         except ObjectDoesNotExist:
#             # Handle the case where a friend ID does not correspond to an existing user
#             pass

#     return render(request, "showFriends.html", {"friends": friends})

# @login_required
# @require_POST
# def addFriend(request):
#     try:
#         data = json.loads(request.body)
#         User = get_user_model()
#         friend_id = data.get('friend_id')

#         if friend_id == request.user.pk:
#             return JsonResponse({"error": "You cannot add yourself as a friend."}, status=400)

#         if friend_id in request.user.friends:
#             return JsonResponse({"error": "This user is already your friend."}, status=400)

#         friend = User.objects.get(pk=friend_id)  # Ensure you're using primary key lookup

#         # If friends field is not initialized
#         if not request.user.friends:
#             request.user.friends = []

#         request.user.friends.append(friend.pk)  # Add friend
#         request.user.save()

#         return JsonResponse({
#             "success": "Friend added",
#             "friend_id": friend.pk,
#             "display_name": friend.display_name,  # Assuming username is the display name
#             "online": friend.online
#         }, status=200)
#     except User.DoesNotExist:
#         return JsonResponse({"error": "Friend not found"}, status=404)
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON"}, status=400)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)


# def changeAvatar(request):
#     User = get_user_model()
#     if request.user.is_authenticated:
#         user = User.objects.get(username=request.user.username)  # Ensure you're using the correct attribute for username
#         if request.method == 'POST':
#             avatar_url = request.POST.get('avatar_url', '').strip()
#             uploaded_file = request.FILES.get('avatar_file')
#             selected_avatar = request.POST.get('static_avatar')

#             if avatar_url:
#                 # Handle URL input
#                 user.avatar_url = avatar_url
#             elif uploaded_file:
#                 # Handle file upload
#                 fs = FileSystemStorage()  # Use MEDIA_ROOT for storage
#                 file_name = fs.save(uploaded_file.name, uploaded_file)
#                 uploaded_file_url = fs.url(file_name)
#                 user.avatar_url = request.build_absolute_uri(uploaded_file_url)
#             elif selected_avatar:
#                 # Handle static file selection
#                 robot_avatars_path = os.path.join(settings.STATIC_ROOT, 'img', 'Robot')
#                 if selected_avatar in os.listdir(robot_avatars_path):
#                     user.avatar_url = os.path.join(settings.STATIC_URL, 'img', 'Robot', selected_avatar)

#             user.last_modified = now()
#             user.save()
#             return render(request=request, template_name="profile.html", context={"user": user})
#         else:
#             # List available .png avatars from static folder with URLs for preview
#             robot_avatars_path = os.path.join(settings.STATIC_ROOT, 'img', 'Robot')
#             robot_avatars_url = os.path.join(settings.STATIC_URL, 'img', 'Robot')
#             available_avatars = [(file, os.path.join(robot_avatars_url, file))
#                                  for file in os.listdir(robot_avatars_path)
#                                  if os.path.isfile(os.path.join(robot_avatars_path, file)) and file.endswith('.png')] if os.path.isdir(robot_avatars_path) else []
#             return render(request, 'changeAvatar.html', {'user': user, 'available_avatars': available_avatars})
#     else:
#         messages.error(request, 'You are not signed in! Please sign in to edit your profile.')
#         return redirect('signIn')

