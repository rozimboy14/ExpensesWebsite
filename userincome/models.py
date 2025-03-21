from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class UserIncome(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source =models.CharField(max_length=280)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']
class Source(models.Model):
    name = models.CharField(max_length=280)
    def __str__(self):
        return self.name
