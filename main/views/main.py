from django.shortcuts import render, redirect
from django.forms import ModelForm
from ..models import *
from django.conf import settings as cfg

from django.db.models import Q
from django.core.paginator import Paginator

from lazysignup.templatetags.lazysignup_tags import *
import random

from django.http import HttpResponseRedirect

import stripe

from django.core.mail import send_mail


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


def notes(request, sender = None, recipient = None, editmode = False, noteID = None, from_learning = False):

    try:
        request.user.profile
    except:
        return redirect('login')
    profile = request.user.profile
    try:
        collection = profile.collection
    except:
        collection = Collection.objects.create(profile=profile)

    # if note is opened from learning mode, it might not be opned
    if from_learning:
        note = Note.objects.get(id=noteID)
        collection.openNotes.add(note)

    form = None
    if editmode:
        # Form is getting saved
        if request.method == 'POST':
            if noteID:
                note = Note.objects.get(id=noteID)
                form = NoteForm(request.POST, instance=note)

                learning_object = note.learning_data
            else:
                form = NoteForm(request.POST)
                learning_object = LearningData.objects.create(profile=profile)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.learning_data = learning_object
                obj.profile = request.user.profile

                obj.save()
                # ensure the new note is open and on top of the recent list
                return redirect("/open/{}/notes".format(obj.id))
        # Form is only getting rendered, not saved
        else:
            if noteID:
                form = NoteForm(instance=Note.objects.get(id=noteID))
            else:
                form = NoteForm()

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

    allNotes = Note.objects.filter(profile=request.user.profile).order_by('-id')

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

    n, created = Note.objects.get_or_create(title = "Welcome", content=WelcomeNote, profile=profile)

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

    collection.save()
    return redirect('/notes')

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

def openNote(request, noteID, redirectPath):
    try:
        request.user.profile
    except:
        return redirect('login')
    # TODO: Slimmer random method
    if noteID == "-":
        notes_keys = Note.objects.filter(profile=request.user.profile).values_list('pk', flat=True)
        random_key = random.choice(notes_keys)
        note = Note.objects.get(id=random_key)
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

    note = Note.objects.get(id=noteID, profile=request.user.profile)
    note.learning_data.delete()
    note.delete()
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
