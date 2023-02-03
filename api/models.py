from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Meal(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField(max_length=255)

    def number_of_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        return len(ratings)

    def average_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        average = sum([i.stars for i in ratings]) / len(ratings) if len(ratings) > 0 else 0 
        return average

    def __str__(self):
        return self.title

class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        indexes  = [
            models.Index(fields=['user', 'meal']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['user', 'meal'], name='user_meal'),
        ]

