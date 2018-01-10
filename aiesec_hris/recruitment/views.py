from django.shortcuts import render

from .forms import ApplicantForm


def register(request):
    form = ApplicantForm

    context_dictionary = {
        'form': form
    }

    return render(request, 'recruitment/applicant_form.html', context=context_dictionary)
