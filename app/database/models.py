from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# class User(models.Model):
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique=True, blank=True)
    name = models.CharField(max_length=50, default='Name')
    surname = models.CharField(max_length=50, default='Surname')
    email = models.EmailField(max_length=100, unique=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    avatar_url = models.URLField(default='https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png')
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    online = models.BooleanField(default=False)
    friends = models.JSONField(default=list)

    def __str__(self):
        return self.username


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    pong_tournament = models.BooleanField(default=False)
    memory_tournament = models.BooleanField(default=False)
    number_of_participants = models.IntegerField(default=0)
    participants = models.ManyToManyField(User)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='won_tournaments')


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    is_tournament = models.BooleanField(default=False)
    pong_game = models.BooleanField(default=False)
    scoreToDo = models.IntegerField(default=0)
    memory_game = models.BooleanField(default=False)
    chosen_set = models.CharField(default='not_defined')
    number_of_cards = models.IntegerField(default=0)
    participants = models.ManyToManyField(User, related_name='games_participated')
    game_date = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='won_games')
    score_winner = models.IntegerField(default=0)
    score_loser = models.IntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name='tournament_games')

