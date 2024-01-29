from django.db import models

# Create your models here.

class Score(models.Model):
    name = models.CharField(max_length=255)
    game = models.CharField(max_length=255)
    date = models.DateField()
    score = models.BooleanField()
    ranking = models.IntegerField()

    def __str__(self):
        return f"{self.name}'s score in {self.game} on {self.date}"
