from django.shortcuts import render, redirect
from django.db.models import Q
from ..models import *

import random
from django.utils import timezone

from supermemo2 import SMTwo, mon_day_year
import datetime

def remove_learning_object(request, pk):
    profile = request.user.profile
    collection = profile.collection

    learning_object = LearningData.objects.filter(profile=profile, id=pk).first()
    learning_object.delete()

    return redirect("/learning")

def open_new_learning_object(request):
    profile = request.user.profile
    collection = profile.collection

    # make a static learning queue for a certain time span
    # whole days would be icky, because of timezones and stuff
    # so we just get 20 new ones and all those we actually should learn today
    # and if it's empty, same thing again
    if not collection.current_learning_objects.exists():
        collection.learning_block_created_at = datetime.datetime.now(datetime.timezone.utc)
        # max. half of the learning block data may be new
        new = LearningData.objects.filter(profile=profile, score__isnull=True)[:((collection.learning_block_size / 2))]
        date_cutoff = datetime.date.today() + datetime.timedelta(days=1)
        current = LearningData.objects.filter(profile=profile, review_date__lt = date_cutoff, score__isnull=False)[:(int(collection.learning_block_size / 2))]
        collection.current_learning_objects.add(*new)
        collection.current_learning_objects.add(*current)

        # we just always make the learning block bigger.
        # if this part of the code gets triggered by the learning block getting stale
        # so that we want to make it smaller, we will just counteract the increase in the given function
        collection.learning_block_size += 2
        collection.save()

    # if still empty, there is nothing left to learn
    if not collection.current_learning_objects.exists():
        return redirect("/")

    learning_objects_key = collection.current_learning_objects.values_list('pk', flat=True)
    random_key = random.choice(learning_objects_key)
    learning_object = LearningData.objects.get(id=random_key)

    collection.open_learning_object = learning_object
    collection.save()

    return redirect ("/learning")



def learning_queue(request, show_backsite):
    profile = request.user.profile
    collection = profile.collection

    learning_object = collection.open_learning_object

    # check how stale the learning data is and resize the block for motivation
    if (timezone.now() - collection.learning_block_created_at) > datetime.timedelta(hours=12):
        collection.learning_block_size = max(8, int(collection.learning_block_size / 2))
        collection.learning_block_size -= 2
        collection.current_learning_objects.clear()
        collection.open_learning_object = None
        collection.save()
        return redirect("/learning/get_new")

    if not learning_object or not collection.current_learning_objects.exists():
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

        collection.current_learning_objects.remove(learning_object)
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
        'note': note,
        'front_site': front_site,
        'back_site': back_site,
        'show_backsite': show_backsite,
        'review_date': learning_object.review_date,
        'count': collection.current_learning_objects.count(),
        'count_new': collection.current_learning_objects.filter(score__isnull=True).count(),
    }

    return render(request, 'learning/queue.html', context)
