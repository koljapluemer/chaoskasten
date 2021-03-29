from ..models import *
from django.shortcuts import render, redirect
import os
from django.conf import settings as settings_conf

from django.contrib.auth import (
    authenticate, get_user_model, password_validation, login
)


def profile(request):
    user = request.user
    context = {}

    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    if not user.profile.has_free_account:
        if user.profile.stripeID != '1':
            created = stripe.Customer.retrieve(user.profile.stripeID).subscriptions.data[0]["created"]
            createdAsDate = datetime.utcfromtimestamp(created).strftime('%Y-%m-%d %H:%M')
            context['created'] = createdAsDate

    context['noteCounter']: user.profile.note_set.all().count()

    return render(request, 'pages/profile.html', context)

def signup(request):
    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/payment_form')
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})

def changeEmail(request):
    user = request.user
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('/profile')
    else:
        form = EmailChangeForm()
    return render(request, 'registration/email_change.html', {'form': form})

def deleteUser(request):
    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    user = request.user
    if not user.profile.has_free_account:
        if user.profile.stripeID != '1':
            stripe.Customer.delete(user.profile.stripeID)
    user.delete()

    return redirect('/')
