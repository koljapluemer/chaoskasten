from ..models import *
from django.shortcuts import render, redirect
from lazysignup.decorators import allow_lazy_user
from django.utils import timezone
from datetime import timedelta

# The landing page
@allow_lazy_user
def home(request):
    # redirect a user to his notes if he has any (excluding the automatic welcome note)
    profile=request.user.profile

    if profile.note_set.all().count() > 1 or (profile.note_set.all().count() == 1 and profile.note_set.first().title != "Welcome"):
        return redirect('/notes')
    else:
        profile=request.user.profile
        if request.method == 'POST':
            d = Drawer.objects.create(name=request.POST.get('drawer'), profile=profile)
            n = Note.objects.create(title=request.POST.get('title'), content=request.POST.get('content'), profile=profile)
            profile.collection.openNotes.add(n)
            profile.save()
            return redirect('/notes')
        return render(request, 'pages/index.html', {})

def about(request):
    stats = {
        'countNotes': Note.objects.exclude(title = "Welcome").count(),
        'countLoginsWeekly': User.objects.filter(last_login__gt = timezone.now() - timedelta(days=7)).count()
    }
    return render(request, 'pages/about.html', stats)
