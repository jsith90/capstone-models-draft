from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

SEAT_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)
TIME_CHOICES = (
    ("1 PM", "1 PM"),
    ("3 PM", "3 PM"),
    ("5 PM", "5 PM"),
    ("7 PM", "7 PM"),
    ("9 PM", "9 PM"),
)

class Table_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    seats = models.CharField(max_length=50, choices=SEAT_CHOICES, default="1")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=5, choices=TIME_CHOICES, default="1 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"