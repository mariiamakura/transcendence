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
    # birthdate = models.DateField(default='2000-01-01')
    # password_hash = models.CharField(max_length=255)
    pong_games_played = models.IntegerField(default=0)
    pong_games_won = models.IntegerField(default=0)
    pong_win_streak = models.IntegerField(default=0)
    pong_tournaments_won = models.IntegerField(default=0)
    memory_games_played = models.IntegerField(default=0)
    memory_games_won = models.IntegerField(default=0)
    memory_win_streak = models.IntegerField(default=0)
    memory_tournaments_won = models.IntegerField(default=0)
    # wallet_id = models.CharField(max_length=42, unique=True, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    avatar_url = models.URLField(default='https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png')
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    online = models.BooleanField(default=False)
    friends = models.JSONField(default=list)

    def __str__(self):
        return self.username

# def save(self, *args, **kwargs):
#     if not self.display_name:
#         self.display_name = self.username
#     super(User, self).save(*args, **kwargs)


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    tournament_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='won_tournaments')
    game_ids = models.JSONField()


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    game_date = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='won_games')
    participants = models.JSONField()
    is_tournament = models.BooleanField(default=False)
