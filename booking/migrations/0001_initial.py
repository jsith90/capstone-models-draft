# Generated by Django 4.2.11 on 2024-03-12 14:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Table_Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], default='1', max_length=50)),
                ('day', models.DateField(default=datetime.datetime.now)),
                ('time', models.CharField(choices=[('1 PM', '1 PM'), ('3 PM', '3 PM'), ('5 PM', '5 PM'), ('7 PM', '7 PM'), ('9 PM', '9 PM')], default='1 PM', max_length=5)),
                ('time_ordered', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
