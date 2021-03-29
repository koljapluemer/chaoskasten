from django.shortcuts import render, redirect
from django.db.models import Q
from ..models import *

from supermemo2 import SMTwo, mon_day_year
from django.utils.timezone import localtime, now


def remove_learning_object(request, pk):
    profile = request.user.profile
    collection = profile.collection

    learning_object = LearningData.objects.filter(profile=profile, id=pk).first()
    learning_object.delete()

    return redirect("/learning")

def learning_queue(request):
    profile = request.user.profile
    collection = profile.collection

    # handle form submittal
    # meaning the user answering how hard a given note was
    if request.method == 'POST':
        # print(request.POST["note-id"] + ": " + request.POST["easiness"])
        old_note = Note.objects.get(id=int(request.POST["note-id"]))
        old_learning_object = old_note.learning_data
        # check whether the card already has learning data, act accordingly
        review = ""
        if old_learning_object.easiness:
            review = SMTwo(
                old_learning_object.easiness,
                old_learning_object.interval,
                old_learning_object.repetitions
            ).review(int(request.POST["easiness"]))
        else:
            review = SMTwo.first_review(int(request.POST["easiness"]))


        old_learning_object.easiness = review.easiness
        old_learning_object.interval = review.interval
        old_learning_object.repetitions = review.repetitions
        old_learning_object.review_date = review.review_date
        old_note.save()

        score = Score.objects.create(value = review.easiness, learning_data=old_learning_object)
        print(old_learning_object.score_set.all())

        return redirect ("/learning")

    # handle getting of new note

    has_learning_items_left = True

    today = localtime(now()).date()
    # try getting todays data, otherwise just get all, sorted by date
    learning_objects = LearningData.objects.filter(review_date = today, profile=profile)
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
