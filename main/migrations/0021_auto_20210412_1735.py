# Generated by Django 2.2.7 on 2021-04-12 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210404_0740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='openDrawer',
        ),
        migrations.RemoveField(
            model_name='note',
            name='drawer',
        ),
        migrations.DeleteModel(
            name='Drawer',
        ),
    ]