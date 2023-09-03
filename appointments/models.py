from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Day(models.Model):
    """
    Represents a single day's appointment booking status. Only one booking per
    day is currently supported.

    Fields:
      - date: The day's date.
      - email: The email of the person who booked the day (if booked).
      - busy: A boolean indicating if the day is booked.
      - first_name: First name of the person who booked the day.
      - last_name: Last name of the person who booked the day.
      - message: Additional message provided at the time of booking.
      - phone: Contact number of the person who booked the day.
      - client: ForeignKey to the registered user who booked the appointment.
    """

    date = models.DateField()
    email = models.EmailField(max_length=254, blank=True)
    busy = models.BooleanField(default=False)
    first_name = models.CharField(null=True, blank=True, max_length=254)
    last_name = models.CharField(null=True, blank=True, max_length=254)
    message = models.CharField(null=True, blank=True, max_length=1800)
    phone = models.CharField(null=True, blank=True, max_length=20)
    client = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return f"{self.date} {self.email if self.email else 'Open Day'}"
