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
    path('showHome', views.showHome, name='showHome'),
    path('showChat', views.showChat, name='ShowChat'),
    path('gamePong', views.gamePong, name='gamePong'),
    path('callback', views.callback, name='callback'),
    path('changeAvatar', views.changeAvatar, name='changeAvatar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
