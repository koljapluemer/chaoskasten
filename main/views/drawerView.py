from django.shortcuts import render, redirect
from django.db.models import Q
from ..models import *

def drawerView(request):
    profile = request.user.profile
    collection = profile.collection

    drawers = Drawer.objects.filter(profile=profile)

    allNotes = Note.objects.filter(profile=request.user.profile).order_by('-id')

    if collection.openDrawer:
        allNotes = allNotes.filter(drawer=Drawer.objects.filter(profile=profile, name=collection.openDrawer).first())

    if collection.searchTerm:
        allNotes = allNotes.filter(Q(content__icontains=collection.searchTerm) | Q(title__icontains=collection.searchTerm))

    context = {
        'notes': allNotes,
        'drawers': drawers,
        'openDrawer': collection.openDrawer,
        'searchTerm': collection.searchTerm,
    }

    return render(request, 'drawerView.html', context)

def drawerSearch(request):
    profile = request.user.profile
    collection = profile.collection
    # set search term
    collection.searchTerm = request.GET.get('searchTerm')
    print(collection.searchTerm)
    # set drawer filter
    if Drawer.objects.filter(profile=profile, name=request.GET.get('drawer')):
        collection.openDrawer = Drawer.objects.filter(profile=profile, name=request.GET.get('drawer')).first()
    else:
        collection.openDrawer = None

    collection.save()
    return redirect('/drawerView')
