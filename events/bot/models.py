from django.db import models
import api.models as api_models


CHOICES = ('1', 'За день'), ('3', 'За три дня'), ('7', 'За неделю')

class Notification(models.Model):
    booking = models.ForeignKey(api_models.Booking, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=200, choices=CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'