from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

from django.db.models.signals import post_save
from django.dispatch import receiver

import stripe

from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Only used when you have to restore your password. Never sold, never spammed.')

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeID = models.TextField()



class CollectionHistory(models.Model):
    addedAt = models.DateTimeField(auto_now_add=True, blank=True)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)



# Update our corresponding Profile model when the boilerplate User changes
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        stripe.api_key = 'sk_test_saz48OVpTahMj8ZhFNKu4PBo00tqeXobcv'
        p = Profile.objects.create(user=instance)
        customer = stripe.Customer.create(
            description="",
            name="",
        )
        p.stripeID = customer.id
        p.save()
        c = Collection.objects.create(profile=p)
        d = Drawer.objects.create(name="Help", profile=p)
        n = Note.objects.create(
            title="Welcome",
            content = WelcomeNote,
            drawer = d,
            profile=p)
        c.openNotes.add(n)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.profile.collection.save()