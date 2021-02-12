from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

from django.db.models.signals import post_save
from django.dispatch import receiver

import stripe

from django import forms


WelcomeNote = """
Create a new note by clicking the `New Note` Button on one of the desks.

With an open note itself you can do the following:

* `Pin:` Your note will be displayed in the "Pinned" section in the sidebar, allowing you quick access at any time
* `Connect:` By clicking the *Connect* button, you can connect two notes with each other, creating references to each other on each note. This is the primary tool to organize your knowledge - try it!
* `Delete:` You may delete the note - but watch out, this cannot be undone. You can this note as a test run, since you can always get a new *Welcome Note* in the `Settings`.
* `Edit:` Change the properties of your notes at anytime. You can test the function with this very note you are reading to find out how all the fancy formatting tricks work (Spoiler: It's Markdown)

To manage your drawers, you may want to check out the `Settings` link.

### Happy productivity!
"""

class Drawer(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    def save_model(self, request, obj, form, change):
        obj.profile = request.user.profile
        super().save_model(request, obj, form, change)

class Note(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank="true", null="true")
    reference = models.ManyToManyField('self')
    drawer = models.ForeignKey('Drawer', on_delete=models.CASCADE, null=True)

class Collection(models.Model):
    openNotes = models.ManyToManyField('Note', related_name="openNotes", blank=True)
    openDrawer = models.ForeignKey('Drawer', null=True, on_delete=models.SET_NULL)

    pinnedNotes = models.ManyToManyField('Note', related_name="pinnedNotes", blank=True)
    recentNotes = models.ManyToManyField('Note', related_name="recentNotes", blank=True, through='CollectionHistory')

    pinnedNotesPageNr = models.IntegerField(default = 1)
    recentNotesPageNr = models.IntegerField(default = 1)
    allNotesPageNr = models.IntegerField(default = 1)

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    searchTerm = models.TextField(blank="true", null="true")

    sidebarCollapsed = models.BooleanField(default=False)