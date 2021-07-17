from django import forms

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings as cfg

from django.db.models.signals import post_save
from django.dispatch import receiver

import stripe
from django.utils import timezone

WelcomeNote = """
Create a new Note by clicking the `New Note` button.

With an open Note itself you can do the following:

* `Favorite:` Your Note will be displayed in the "Favorite" section in the sidebar, allowing you quick access at any time
* `Connect:` By clicking the *Connect* button, you can connect two Notes with each other, creating references to each other on each Note. This is the primary tool to organize your knowledge - try it!
* `Delete:` You may delete the Note - but watch out, this cannot be undone. You can this Note as a test run, since you can always get a new *Welcome Note* in the `Settings`.
* `Edit:` Change the properties of your Notes at anytime. You can test the function with this very Note you are reading to find out how all the fancy formatting tricks work (Spoiler: It's Markdown)

### Happy productivity!
"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_free_account = models.BooleanField(default=False)
    stripeCustomerID = models.TextField()

class Score(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    value = models.IntegerField()
    learning_data = models.ForeignKey('LearningData', on_delete=models.CASCADE)


class LearningData(models.Model):
    easiness = models.FloatField(null=True)
    interval = models.IntegerField(null=True)
    repetitions = models.IntegerField(null=True)
    review_date = models.DateTimeField(null=True, auto_now_add=True)

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Note(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank="true", null="true")
    reference = models.ManyToManyField('self')

    learning_data = models.OneToOneField(LearningData, null=True, on_delete=models.SET_NULL)

    def isNoteOpen(self):
        if self.openNotes.all().count() == 0:
            return False
        else:
            return True


class Collection(models.Model):
    openNotes = models.ManyToManyField('Note', related_name="openNotes", blank=True)

    pinnedNotes = models.ManyToManyField('Note', related_name="pinnedNotes", blank=True)
    recentNotes = models.ManyToManyField('Note', related_name="recentNotes", blank=True, through='CollectionHistory')
    noteConnectionSender = models.ForeignKey('Note', null=True, on_delete=models.SET_NULL)

    open_learning_object = models.ForeignKey('LearningData', null=True, on_delete=models.SET_NULL)
    current_learning_objects = models.ManyToManyField('LearningData', related_name="learning_queue")
    learning_block_size = models.IntegerField(default = 20)
    learning_block_created_at = models.DateTimeField(blank=True, default=timezone.now())

    pinnedNotesPageNr = models.IntegerField(default = 1)
    recentNotesPageNr = models.IntegerField(default = 1)
    allNotesPageNr = models.IntegerField(default = 1)

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    searchTerm = models.TextField(blank="true", null="true")
    search_only_removed_from_learning = models.BooleanField(default=False)

    sidebarCollapsed = models.BooleanField(default=False)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Only used for confirmation or when you have to restore your password. Never sold, never spammed.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def get_credentials(self):
        return {
            "username": self.cleaned_data["username"],
            "password": self.cleaned_data["password1"]
        }


class EmailChangeForm(forms.Form):
    email = forms.EmailField(label='New Email adress')


class CollectionHistory(models.Model):
    addedAt = models.DateTimeField(auto_now_add=True, blank=True)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)


# Update our corresponding Profile model when the boilerplate User changes
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        stripe.api_key = cfg.STRIPE_SECRET_KEY
        p = Profile.objects.create(user=instance)
        customer = stripe.Customer.create(
            description="",
            name="",
        )
        p.stripeCustomerID = customer.id
        p.save()
        c = Collection.objects.create(profile=p)
        n = Note.objects.create(
            title="Welcome",
            content = WelcomeNote,
            profile=p)
        c.openNotes.add(n)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.profile.collection.save()
