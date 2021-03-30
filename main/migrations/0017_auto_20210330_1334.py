# Generated by Django 2.2.7 on 2021-03-30 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20210329_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='learning_objects',
        ),
        migrations.AddField(
            model_name='collection',
            name='open_learning_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.LearningData'),
        ),
    ]
