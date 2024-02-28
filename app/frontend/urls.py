from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('signUp', views.signUp, name='signUp'),
    path('signIn', views.signIn, name='signIn'),
    path('signOut', views.signOut, name='signOut'),
    path('showProfile', views.showProfile, name='ShowProfile'),
    path('editProfile', views.editProfile, name='editProfile'),
    path('showHome', views.showHome, name='ShowHome'),

]
# urlpatterns = [
#     path('signup/', views.signup_view, name='signup'),  # Endpoint for sign-up form
#     path('signup_endpoint/', views.signup_view, name='signup'),
# ]
