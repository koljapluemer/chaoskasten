# Generated by Django 2.2.7 on 2021-03-05 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_profile_payment_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='payment_confirmed',
        ),
    ]
