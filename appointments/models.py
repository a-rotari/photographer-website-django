from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Day(models.Model):
    date = models.DateField()
    email = models.EmailField(max_length=254, blank=True)
    busy = models.BooleanField(default=False)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(null=True, blank=True, max_length=254)
    message = models.CharField(null=True, blank=True, max_length=1800)
    phone = models.CharField(null=True, blank=True, max_length=20)
    client = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return str(self.date) + ' ' + self.email
