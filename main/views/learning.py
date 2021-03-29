from django.shortcuts import render, redirect
from django.db.models import Q
from ..models import *

from supermemo2 import SMTwo, mon_day_year
from django.utils.timezone import localtime, now


def learning_queue(request):
    profile = request.user.profile
    collection = profile.collection

    print("_________")
    for o in LearningData.objects.filter(profile=profile):
        print(o.note.title)
        print(o.easiness)
        print(o.review_date)
        print("_________")

    # handle form submittal
    # meaning the user answering how hard a given note was
    if request.method == 'POST':
        # print(request.POST["note-id"] + ": " + request.POST["easiness"])
        old_note = Note.objects.get(id=int(request.POST["note-id"]))
        old_learning_object = old_note.learning_data
        print("TITLE OF PARENT: ", old_learning_object.note.title)
        # check whether the card already has learning data, act accordingly
        review = ""
        if old_learning_object.easiness:
            print("exists")
            review = SMTwo(
                old_learning_object.easiness,
                old_learning_object.interval,
                old_learning_object.repetitions
            ).review(int(request.POST["easiness"]))
        else:
            print("new")
            review = SMTwo.first_review(int(request.POST["easiness"]))

        print(review)

        old_learning_object.easiness = review.easiness
        old_learning_object.interval = review.interval
        old_learning_object.repetitions = review.repetitions
        old_learning_object.review_date = review.review_date
        print("SAVE: ", old_learning_object.save())
        old_note.save()
        print("CHECK VIA NOTE: ", old_note.learning_data.easiness)

        return redirect ("/learning")

    # handle getting of new note

    has_learning_items_left = True

    today = localtime(now()).date()
    # try getting todays data, otherwise just get all, sorted by date
    learning_objects = LearningData.objects.filter(review_date = today, profile=profile)
    print(today)
    if not learning_objects:
        learning_objects = LearningData.objects.filter(profile=profile).order_by('review_date')
        has_learning_items_left = False

    learning_object = learning_objects.first()

    note = learning_object.note


    context = {
        'note': note,
        'has_learning_items_left': has_learning_items_left
    }

    return render(request, 'learning/queue.html', context)
