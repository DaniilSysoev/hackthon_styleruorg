from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    is_stuff = models.BooleanField(default=False)
    telegram = models.CharField(max_length=200, blank=True, null=True)
    telegram_id = models.IntegerField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(default='12:00:00')

    def __str__(self):
        return self.title


class Booking(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.event_id.title