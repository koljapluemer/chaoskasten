# Generated by Django 2.2.7 on 2021-03-29 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_learningdata_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('value', models.IntegerField()),
                ('learning_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.LearningData')),
            ],
        ),
    ]
