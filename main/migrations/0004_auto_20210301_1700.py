# Generated by Django 2.2.7 on 2021-03-01 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_profile_stripesubscriptionid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='stripeID',
            new_name='stripeCustomerID',
        ),
    ]
