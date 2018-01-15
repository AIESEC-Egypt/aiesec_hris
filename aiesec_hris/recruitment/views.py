from django.shortcuts import render

from .forms import ApplicantForm


def register(request):
    context_dictionary = {}

    if request.method == "POST":
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.save()

            print('Success')
    else:
        form = ApplicantForm()
    # errors = form.errors
    # context_dictionary.update({'errors': errors})

    context_dictionary.update({
        'form': form,
    })

    return render(request, 'recruitment/applicant_form.html', context=context_dictionary)
