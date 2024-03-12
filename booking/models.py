from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

TABLE_CHOICES = (
    ("Table 1 (2 seats)", "Table 1 (2 seats)"),
    ("Table 2 (2 seats)", "Table 2 (2 seats)"),
    ("Table 3 (2 seats)", "Table 3 (2 seats)"),
    ("Table 4 (4 seats)", "Table 4 (4 seats)"),
    ("Table 5 (4 seats)", "Table 5 (4 seats)"),
    ("Table 6 (4 seats)", "Table 6 (4 seats)"),
    ("Table 7 (8 seats)", "Table 7 (8 seats)"),
    ("Table 8 (8 seats)", "Table 8 (8 seats)"),
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
    table = models.CharField(max_length=50, choices=TABLE_CHOICES, default="Table 1 (2 seats)")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=5, choices=TIME_CHOICES, default="1 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time} | table: {self.table}" 