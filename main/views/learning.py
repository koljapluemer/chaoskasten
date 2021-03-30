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

def open_new_learning_object(request):
    profile = request.user.profile
    collection = profile.collection

    learning_objects = LearningData.objects.filter(profile=profile).order_by('review_date')
    learning_object = learning_objects.first()

    collection.open_learning_object = learning_object
    collection.save()

    return redirect ("/learning")



def learning_queue(request, show_backsite):
    profile = request.user.profile
    collection = profile.collection

    learning_object = collection.open_learning_object

    if not learning_object:
        return redirect("/learning/get_new")

    # handle form submittal
    # meaning the user answering how hard a given note was
    if request.method == 'POST':
        # check whether the card already has learning data, act accordingly
        review = ""
        if learning_object.easiness:
            review = SMTwo(
                learning_object.easiness,
                learning_object.interval,
                learning_object.repetitions
            ).review(int(request.POST["easiness"]))
        else:
            review = SMTwo.first_review(int(request.POST["easiness"]))


        learning_object.easiness = review.easiness
        learning_object.interval = review.interval
        learning_object.repetitions = review.repetitions
        learning_object.review_date = review.review_date
        learning_object.save()

        score = Score.objects.create(value = review.easiness, learning_data=learning_object)

        return redirect ("/learning/get_new")

    note = learning_object.note

    # check how much seperators the note has, and adapt the preview accordingly
    content_divided = note.content.split("---")
    area_count = len(content_divided)
    if area_count == 1:
        front_site = ""
        back_site = note.content
    else:
        front_site = content_divided[-2]
        back_site = content_divided[-1]

    context = {
        'title': note.title,
        'front_site': front_site,
        'back_site': back_site,
        'show_backsite': show_backsite,
        'review_date': learning_object.review_date
    }

    return render(request, 'learning/queue.html', context)
