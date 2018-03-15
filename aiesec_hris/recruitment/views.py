from django.contrib import messages
from django.db.models import Avg, F
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ApplicantForm
from .models import Timeline, Applicant


def register(request):
    context_dictionary = {}

    if request.method == "POST":
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            timeline = Timeline()
            timeline.save()
            applicant.timeline = timeline
            applicant.save()
            return redirect('recruitment:registration-complete')
    else:
        form = ApplicantForm()
    # errors = form.errors
    # context_dictionary.update({'errors': errors})

    context_dictionary.update({
        'form': form,
    })

    return render(request, 'recruitment/applicant_form.html', context=context_dictionary)


def applicant_profile(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    context_dictionary = {
        'applicant': applicant
    }
    return render(request, 'recruitment/applicant_profile.html', context_dictionary)


def applicant_contacted(request, applicant_id):
    applicant = get_object_or_404(Applicant, pk=applicant_id)
    # if request.user == 'MC':
    applicant.contact(request.user)
    messages.success(request, 'Applicant Contacted Successfully!', extra_tags='alert-success')

    return redirect('recruitment:applicant-profile', applicant_id)


def recruitment_list(request):
    context_dictionary = {}
    applicants = Applicant.objects.all()
    process_time = applicants.aggregate(
        average_difference=Avg(F('timeline__date_contacted') - F('timeline__date_applied')))
    print(process_time)
    context_dictionary.update({
        'applicants': applicants,
        'process_time': process_time
    })
    return render(request, 'recruitment/recruitment_list.html', context_dictionary)


def registration_complete(request):
    return render(request, 'recruitment/registration_successful.html')
