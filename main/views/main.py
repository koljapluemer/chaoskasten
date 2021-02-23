from django.shortcuts import render, redirect
from django.forms import ModelForm
from ..models import *

from django.db.models import Q
from django.core.paginator import Paginator

from lazysignup.templatetags.lazysignup_tags import *
import random

from django.http import HttpResponseRedirect

# after the connection is made or the user aborts
def deactiveConnectionMode(request):
    try:
        request.user.profile
    except:
        return redirect('login')

    profile = request.user.profile
    collection = profile.collection

    collection.noteConnectionSender = None;
    collection.save()

    return redirect('/notes')

# when the user wants to connect a note, we temporarily store the "sending" note in the db
# maybe this will fix the weird bug where images not loading
def activateConnectionSender(request, sender):
    try:
        request.user.profile
    except:
        return redirect('login')

    if not request.user:
        return redirect('login')
    profile = request.user.profile
    collection = profile.collection

    collection.noteConnectionSender = Note.objects.filter(id=sender).first()
    collection.save()

    return redirect('/notes')


# attach the note the user just clicked to the one we saved in the database collection
def attachConnectionRecipient(request, recipient):
    try:
        request.user.profile
    except:
        return redirect('login')
    profile = request.user.profile
    collection = profile.collection

    if collection.noteConnectionSender:
        collection.noteConnectionSender.reference.add(Note.objects.get(id = recipient, profile=profile))

    return redirect('/notes/deactiveConnectionMode')


def notes(request, sender = None, recipient = None, editmode = False, noteID = None):
    try:
        request.user.profile
    except:
        return redirect('login')
    profile = request.user.profile
    collection = profile.collection

    form = None
    if editmode:
        # Form is getting saved
        if request.method == 'POST':
            if noteID:
                form = NoteForm(request.POST, instance=Note.objects.get(id=noteID))
            else:
                form = NoteForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.profile = request.user.profile
                obj.save()
                # ensure the new note is open and on top of the recent list
                return redirect("/open/{}/notes".format(obj.id))
        # Form is only getting rendered, not saved
        else:
            if noteID:
                form = NoteForm(instance=Note.objects.get(id=noteID))
                # limit drawer select to only own drawers
                form.fields['drawer'].queryset = Drawer.objects.filter(profile=request.user.profile)
            else:
                form = NoteForm()
                # limit drawer select to only own drawers
                form.fields['drawer'].queryset = Drawer.objects.filter(profile=request.user.profile)
    # All the sidebar list paginators
    # PINNED
    pinnedNotes = collection.pinnedNotes.order_by('-id')
    pinnedNotesPaginator = Paginator(pinnedNotes, 5)
    pinnedNotesPage = pinnedNotesPaginator.get_page(profile.collection.pinnedNotesPageNr)

    # RECENT
    recentNotes = collection.recentNotes.order_by('-collectionhistory')
    recentNotesPaginator = Paginator(recentNotes, 5)
    recentNotesPage = recentNotesPaginator.get_page(profile.collection.recentNotesPageNr)

    # ALL/SEARCH
    # first filter by drawer (if exists), then by search term)

    allNotes = Note.objects.filter(profile=request.user.profile).order_by('-id')

    if collection.openDrawer:
        allNotes = allNotes.filter(drawer=Drawer.objects.filter(profile=profile, name=collection.openDrawer).first())

    if collection.searchTerm:
        allNotes = allNotes.filter(Q(content__icontains=collection.searchTerm) | Q(title__icontains=collection.searchTerm))

    allNotesPaginator = Paginator(allNotes, 5)
    allNotesPage = allNotesPaginator.get_page(profile.collection.allNotesPageNr)

    if collection.noteConnectionSender:
        sender = collection.noteConnectionSender.id

    context = {
        'notes': collection.openNotes.all(),
        'pinnedNotes': pinnedNotesPage,
        'recentNotes': recentNotesPage,
        'allNotes': allNotesPage,
        'sender': sender,
        'form': form,
        'editableNote': noteID,
        'searchTerm': collection.searchTerm,
        'drawers': profile.drawer_set.all(),
        'openDrawer': collection.openDrawer,
        'sidebarCollapsed': collection.sidebarCollapsed,
    }
    return render(request, 'notes.html', context)

def changePage(request, section, pageNr):
    try:
        request.user.profile
    except:
        return redirect('login')
    profile = request.user.profile
    collection = profile.collection

    if section == "pinned":
        collection.pinnedNotesPageNr = pageNr
    elif section == "recent":
        collection.recentNotesPageNr = pageNr
    elif section == "all":
        collection.allNotesPageNr = pageNr

    collection.save()
    return redirect('/notes')

def generateWelcomeNote(request):

    try:
        request.user.profile
    except:
        return redirect('login')
    profile = request.user.profile
    collection = profile.collection

    d, created = Drawer.objects.get_or_create(name="Help", profile=profile)
    n, created = Note.objects.get_or_create(title = "Welcome", content=WelcomeNote, drawer = d, profile=profile)

    collection.openNotes.add(n)

    return redirect('/notes')

def pinNote(request, noteID):
    try:
        request.user.profile
    except:
        return redirect('login')

    profile = request.user.profile
    collection = profile.collection
    note = Note.objects.get(id=noteID, profile=profile)
    collection.pinnedNotes.add(note)
    return redirect('/notes')

def unpinNote(request, noteID):
    try:
        request.user.profile
    except:
        return redirect('login')

    profile = request.user.profile
    collection = profile.collection
    note = Note.objects.get(id=noteID, profile=profile)
    collection.pinnedNotes.remove(note)
    return redirect('/notes')

def unconnectNotes(request, sender = None, recipient = None):
    try:
        request.user.profile
    except:
        return redirect('login')

    profile = request.user.profile
    collection = profile.collection

    try:
        Note.objects.get(id = sender, profile=profile).reference.remove(Note.objects.get(id = recipient, profile=profile))
        return redirect('/notes')
    except:
        return redirect('/notes')

def search(request):
    try:
        request.user.profile
    except:
        return redirect('login')

    profile = request.user.profile
    collection = profile.collection
    # set search term
    collection.searchTerm = request.GET.get('searchTerm')
    # set drawer filter
    if Drawer.objects.filter(profile=profile, name=request.GET.get('drawer')):
        collection.openDrawer = Drawer.objects.filter(profile=profile, name=request.GET.get('drawer')).first()
    else:
        collection.openDrawer = None

    collection.save()
    return redirect('/notes')

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'drawer']

def openNote(request, noteID, redirectPath):
    try:
        request.user.profile
    except:
        return redirect('login')
    # TODO: Slimmer random method
    if noteID == "-":
        notes = Note.objects.filter(profile=request.user.profile)
        note = random.choice(notes)
    else:
        note = Note.objects.get(id=int(noteID), profile=request.user.profile)
    collection = Collection.objects.get(profile=request.user.profile)

    collection.openNotes.add(note)

    collection.recentNotes.remove(note)
    collection.recentNotes.add(note)

    return redirect('/' + redirectPath)

def closeNote(request, noteID, redirectPath):
    try:
        request.user.profile
    except:
        return redirect('login')

    note = Note.objects.get(id=int(noteID), profile=request.user.profile)
    collection = Collection.objects.get(profile=request.user.profile)
    collection.openNotes.remove(note)

    return redirect('/' + redirectPath)


def closeNotes(request):
    try:
        request.user.profile
    except:
        return redirect('login')

    collection = Collection.objects.get(profile=request.user.profile)
    collection.openNotes.clear()
    return redirect('/notes')

def deleteNote(request, noteID):
    try:
        request.user.profile
    except:
        return redirect('login')

    Note.objects.get(id=noteID, profile=request.user.profile).delete()
    return redirect('/notes')

def sidebar(request):
    try:
        request.user.profile
    except:
        return redirect('login')

    profile = request.user.profile
    collection = profile.collection

    collection.sidebarCollapsed = not collection.sidebarCollapsed
    collection.save()

    return redirect('/notes')
