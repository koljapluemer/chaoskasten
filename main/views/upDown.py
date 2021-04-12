from ..models import *
from django.shortcuts import render, redirect

# export data
import csv
from django.http import HttpResponse

def download(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chaosnotes.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'content', 'reference'])
    for note in Note.objects.filter(profile=request.user.profile):
        writer.writerow([note.id, note.title, note.content, list(note.reference.all().values_list('id', flat=True))])
    return response


def upload(request):
    data = {}
    if request.method == "GET" :
        return render(request, "pages/settings.html", data)
    # if not GET, then proceed
    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return render(request, 'pages/settings.html')
    #if file is too large, return
    if csv_file.multiple_chunks():
        messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        return render(request, 'pages/settings.html')

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split('>><<\n')
    for line in lines:
        fields = line.split(",")
        try:
            if not Note.objects.filter(title=fields[1], profile=request.user.profile).exists():
                Note.objects.create(title=fields[1], content=fields[2], profile=request.user.profile)
        except:
            pass

    return render(request, 'pages/settings.html')
