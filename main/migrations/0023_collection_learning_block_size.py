# Generated by Django 2.2.7 on 2021-07-17 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_collection_search_only_removed_from_learning'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='learning_block_size',
            field=models.IntegerField(default=20),
        ),
    ]
