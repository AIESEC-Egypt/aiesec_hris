"""
Accounts Moderation Views
Author: AmrAnwar
"""
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings

from ..models import Profile
from ..forms import DeclineForm


@staff_member_required()
def profile_decline(request, id=None):
    """
    The Method work when a staff Post request in the Decline Form for specific Profile
    if form is valid >> update verification_issue
    :param request:
    :param id: the profile id
    :return: if staff redirect to the moderation list else : 404
    """
    profile = get_object_or_404(Profile, id=id)
    form = DeclineForm(request.POST or None, instance=profile)
    if form.is_valid():
        instance = form.save()
        if not request.GET.get('testing'):
            domain = request.META['HTTP_HOST']
            message = """
            Hello %s,

            Your Profile was declined
            So please login to update your data : %s/login

            Best regards,
            AIESEC Egypt
            """ % (profile.user.first_name, domain)
            send_mail(
                'Profile Declined',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [profile.user.email],
                fail_silently=False,
            )
        messages.success(request, "Profile is Declined")

    else:
        messages.error(request, "Can't decline this profile , error happen")
    return HttpResponseRedirect(reverse("moderation-list"))


@staff_member_required()
def profile_accept(request, id=None):
        """
        redirect method work when the staff click on profile  accept button
        if profile << change verification_issue to None(4)
            then redirect to reverse('moderation-list')
        """
        profile = get_object_or_404(Profile, id=id)
        profile.verification_issue = 4
        profile.save()

        if not request.GET.get('testing'):
            domain = request.META['HTTP_HOST']
            message = """
            Hello %s,

            Your Profile was accepted
            Now you can Login : %s/login
            
            Best regards,
            AIESEC Egypt
            """ % (profile.user.first_name, domain)
            send_mail(
                'Profile Accepted',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [profile.user.email],
                fail_silently=False,
            )

        messages.success(request, message="Profile is Accepted")
        return HttpResponseRedirect(reverse("moderation-list"))


@staff_member_required()
def reviews_list(request):
    """
    //DeclineForm : django form for decline Profiles
    //if verification_issue = 1 << the user is unreviewed
    //if verification_issue = 4 << the user is accepted
    //if verification_issue = 2, 3 << the user is declined
    //decline_status in context to add new col in the Decline table
    """
    form = DeclineForm(request.POST or None)
    search = request.GET.get('search')
    if search:
        profiles = Profile.objects.search(search=search)
    else:
        profiles = Profile.objects.all()
    unreviewed = profiles.filter(verification_issue=1)
    accepted = profiles.filter(verification_issue=4)
    declined = profiles.filter(Q(verification_issue=2) |
                               Q(verification_issue=3))
    context = {
        'unreviewed': unreviewed,
        'accepted': accepted,
        'declined': declined,
        'form': form,
        'fields': ['full_name',
                   'phone',
                   'email',
                   'lc',
                   'position',
                   'date_of_birth',
                   'gender',
                   'expa_id',
                   'national_id_number',
                   'id_picture',
                   ]
    }

    return render(request, "moderation.html", context=context)
