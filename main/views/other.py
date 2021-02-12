from ..models import *
from django.shortcuts import render, redirect

from django.forms.models import modelformset_factory


def settings(request):
    context = {
        'drawers': Drawer.objects.filter(profile=request.user.profile)
    }
    return render(request, 'pages/settings.html', context)


DrawerFormSet = modelformset_factory(Drawer, fields=('name',), extra=2, can_delete=True)

def editDrawers(request):
    if request.method == 'POST':
        formset = DrawerFormSet(data=request.POST)
        instances = formset.save(commit=False)
        for form in formset:
            if form.is_valid():
                obj = form.save(commit=False)
                if obj.name != '':
                    obj.profile = request.user.profile
                    obj.save()
        for obj in formset.deleted_objects:
            Drawer.objects.filter(profile=request.user.profile, name=obj).delete()
        return redirect('/settings')
    else:
        formset = DrawerFormSet(queryset=Drawer.objects.filter(profile=request.user.profile))
    return render(request, 'pages/editDrawers.html', {"formset": formset})