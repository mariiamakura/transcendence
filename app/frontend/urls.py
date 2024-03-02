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
    path('showChat', views.showChat, name='ShowChat'),

]
