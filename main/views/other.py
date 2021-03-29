import stripe

from ..models import *
from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.conf import settings as cfg

def settings(request):
    try:
        profile = request.user.profile
    except:
        return redirect('login')

    if not profile.has_free_account:

        stripe.api_key = cfg.STRIPE_SECRET_KEY
        stripe_id = profile.stripeCustomerID
        stripe_customer = stripe.Customer.retrieve(stripe_id)
        stripe_email = stripe_customer.email
        # TODO: Can a user ever have more than one subscription
        subscription_status = stripe_customer.subscriptions.data[0].status

        context = {
            'drawers': Drawer.objects.filter(profile=request.user.profile),
            'stripe_email': stripe_email,
            'subscription_status': subscription_status,
        }

    else:
        context = {
            'drawers': Drawer.objects.filter(profile=request.user.profile),
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
