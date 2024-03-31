from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'frontend'


urlpatterns = [
    path('', views.home, name='home'),
    path('signUp', views.signUp, name='signUp'),
    path('signIn', views.signIn, name='signIn'),
    path('signOut', views.signOut, name='signOut'),
    path('showProfile', views.showProfile, name='showProfile'),
    path('editProfile', views.editProfile, name='editProfile'),
    path('Home', views.home, name='Home'),
    path('showChat', views.showChat, name='ShowChat'),
    path('gamePong', views.gamePong, name='gamePong'),
    path('callback', views.callback, name='callback'),
    path('changeAvatar', views.changeAvatar, name='changeAvatar'),
    path('showFriends', views.showFriends, name='showFriends'),
    path('searchUsers/', views.searchUsers, name='searchUsers'),
    path('addFriend/', views.addFriend, name='addFriend'),
    path('removeFriends/', views.removeFriends, name='removeFriends'),
    path('scoreboard', views.scoreboard, name='scoreboard'),
    path('home', views.home, name='home'),
    path('gameMemory', views.gameMemory, name='gameMemory'),
    path('update_start_tournament/', views.start_tournament, name='start_tournament'),
    path('update_game_result_pong/', views.update_game_result_pong, name='update_game_result_pong'),
    path('update_game_result_memory/', views.update_game_result_memory, name='update_game_result_memory'),
    # path('switch_language/', views.switch_language, name='switch_language'),
    path('get_display_name/', views.get_display_name, name='get_display_name'),
    path('update_end_tournament/', views.end_tournament, name='update_end_tournament'),
    path('get_user_statistics/', views.get_user_statistics, name='get_user_statistics'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

