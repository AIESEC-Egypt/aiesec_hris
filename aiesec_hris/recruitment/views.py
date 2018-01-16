from django.shortcuts import render, redirect

from .forms import ApplicantForm
from .models import Timeline


def register(request):
    context_dictionary = {}

    if request.method == "POST":
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            timeline = Timeline()
            timeline.status_applied = True
            timeline.save()
            applicant.timeline = timeline
            applicant.save()
            return redirect(registration_complete)
    else:
        form = ApplicantForm()
    # errors = form.errors
    # context_dictionary.update({'errors': errors})

    context_dictionary.update({
        'form': form,
    })

    return render(request, 'recruitment/applicant_form.html', context=context_dictionary)


def registration_complete(request):
    return render(request, 'recruitment/registration_successful.html')
