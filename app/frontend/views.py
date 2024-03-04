# In your app's views.py file

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


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
def home(request):
    return render(request=request, template_name="home.html", context={})


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
            if request.POST.get('birthdate') != "":
                user.birthdate = request.POST.get('birthdate')
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
def showHome(request):
    return render(request=request, template_name="home.html", context={})


@csrf_exempt
def showChat(request):
    return render(request, 'chat.html')
    # return render(request=request, template_name="chat.html", context={})
