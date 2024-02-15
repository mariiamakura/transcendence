from django.db import models

# Create your models here.

# class Score(models.Model):
#     name = models.CharField(max_length=255)
#     game = models.CharField(max_length=255)
#     date = models.DateField()
#     score = models.BooleanField()
#     ranking = models.IntegerField()

#     def __str__(self):
#         return f"{self.name}'s score in {self.game} on {self.date}"

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    intra_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password_hash = models.CharField(max_length=255)
    normal_games_played = models.IntegerField(default=0)
    normal_games_won = models.IntegerField(default=0)
    normal_win_streak = models.IntegerField(default=0)
    tournaments_won = models.IntegerField(default=0)
    date_of_creation = models.DateTimeField(auto_now_add=True)

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


