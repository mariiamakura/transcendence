# In your app's views.py file

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth import get_user_model
# from django.http import JsonResponse
# from django.contrib.auth.models import User
# from django.views.decorators.csrf import csrf_exempt


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
        user = User.objects.create_user(username=username, email=email,
                                        password=password)

        # redirect the user to the home page
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # login the user so they do not have to re enter the same information again
        return redirect("/")

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
            return HttpResponse("fail")

    return render(request=request, template_name="signIn.html", context={})


@csrf_exempt
def home(request):
    return render(request=request, template_name="home.html", context={})


@csrf_exempt
def signOut(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("<strong>logout successful.<a href='signIn'> Go to Login page</a></strong>")
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
def showHome(request):
    return render(request=request, template_name="home.html", context={})
# User = get_user_model()


# def signup_view(request):
#     if request.method == 'POST':
#         # Process the form data
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')

#         # Create a new user instance and save it to the database
#         # new_user = User.objects.create_user(username=username, email=email, password=password)

#         User.set_new_user(username, username, username, email, password)
#         # Redirect to a success page or log in the user
#         return redirect('success')  # Redirect to a success page

#     # If not a POST request, render the sign-up form template
#     return render(request, 'signup.html')


# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')

#         # Validate the form data here

#         user = User.objects.create_user(username, email, password)
#         user.save()

#         return JsonResponse({'message': 'User created successfully'}, status=201)

#     return JsonResponse({'error': 'Invalid method'}, status=400)


# def signup_endpoint(request):
#     if request.method == 'POST':
#         # Process the form data
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')

#         # Create a new user instance and save it to the database
#         # new_user = User.objects.create_user(username=username, email=email, password=password)

#         User.set_new_user(username, username, username, email, password)
#         # Redirect to a success page or log in the user
#         return redirect('success')  # Redirect to a success page

#     # If not a POST request, render the sign-up form template
#     return render(request, 'signup.html')
