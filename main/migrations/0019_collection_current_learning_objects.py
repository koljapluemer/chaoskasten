# Generated by Django 2.2.7 on 2021-04-04 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210330_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='current_learning_objects',
            field=models.ManyToManyField(null=True, related_name='learning_queue', to='main.LearningData'),
        ),
    ]
