from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import FormView
from django.contrib.auth.models import User

from ..models import Profile
from ..forms import ProfileForm
from .mixins import JsonFormInvalidMixin


class RegisterView(JsonFormInvalidMixin, FormView):
    template_name = 'register.html'
    form_class = ProfileForm

    def form_valid(self, form):
        """
        If the form is valid, respond with success
        """
        first_name = form.cleaned_data.pop('first_name')
        last_name = form.cleaned_data.pop('last_name')
        email = form.cleaned_data.pop('email')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email)
        user.save()

        user.set_password(form.cleaned_data.pop('password'))
        user.save()

        form.cleaned_data.update({'user': user})

        profile = Profile(**form.cleaned_data)
        profile.save()

        success_url = 'Registeration Successful, your data will be reviewed and you will be emailed once your data is approved'
        messages.success(self.request, success_url)
        return JsonResponse(
            {'details': success_url, 'success_url': reverse('login')})
