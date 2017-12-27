"""
Profile Update Views for declined profiles
Author: AmrAnwar
"""
import datetime

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.views.generic import FormView

from django.contrib import messages
from django.urls import reverse

from ..models import ResetPasswordCode
from ..forms import ProfileForm
from .mixins import JsonFormInvalidMixin


class ProfileDeclineUpdate(JsonFormInvalidMixin, FormView):
    """
    this Class work when user with decline profile try to login
    """
    form_class = ProfileForm
    template_name = 'register.html'
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_profile_using_code()
        return super(ProfileDeclineUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileDeclineUpdate, self).get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    def get_form(self, form_class=None):
        form = super(ProfileDeclineUpdate, self).get_form()
        form.fields.pop('position')
        form.fields.pop('email')
        return form

    def get_initial(self):
        """
        Returns the initial data to use for the form
        """
        initial = super(ProfileDeclineUpdate, self).get_initial()
        initial['first_name'] = self.profile.user.first_name
        initial['last_name'] = self.profile.user.last_name
        return initial

    def get(self, request, *args, **kwargs):
        """
        get code object at first
            if ( it expired): alert message to login again
            else : return data < form , template >
        :param request:
        :param kwargs: id << profile id
        """
        code = get_object_or_404(ResetPasswordCode, code=self.kwargs['code'])
        if (datetime.datetime.now() - code.created_at >
                datetime.timedelta(minutes=5)):
            context = {
                'message': 'profile update page was expired login in again please',
                'alert_type': 'danger'}
            self.template_name = 'message.html'
            return self.render_to_response(context)
        self.profile = code.user.profile
        return self.render_to_response(self.get_context_data())

    def get_form_kwargs(self):
        """
        add the profile instance data to the form
        :return: the ProfileDeclineUpdate Form with the user data
        """
        form_kwargs = super(ProfileDeclineUpdate, self).get_form_kwargs()
        form_kwargs['instance'] = self.profile
        return form_kwargs

    def form_valid(self, form, **kwargs):
        """
        firstly: will pop('password') and check if it true
                else : return JsonResponse("wrong pass")
        then : save the form data into the profile then redirect to login page
        :param form: our ProfileDeclineUpdate Form get it from Post() method
        :return:
        """
        if self.profile.user.check_password(
                form.cleaned_data.pop('password')):
            user_data = {
                'first_name': form.cleaned_data.pop('first_name'),
                'last_name': form.cleaned_data.pop('last_name'),
            }
            self.profile.user.__dict__.update(user_data)
            self.profile.user.save()

            instance = form.save(commit=False)
            instance.verification_issue = 1
            instance.save()
            details_string = """your profile was updated successfully
            please wait until review it"""
            messages.success(self.request, details_string)
            return JsonResponse({'details': details_string,
                                 'success_url': '%s' % reverse('login'),
                                 })
        return JsonResponse({
            'details': 'you entered wrong password'})

    def post(self, request, *args, **kwargs):
        """
        if form is valid << form_valid method will work
        :param request:
        :return: form_valid(form) if valid
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return JsonResponse({
                'details': 'form is not valid'})

    def get_profile_using_code(self):
        """
        simple method to get profile obj from the code string
        :param self:
        """
        if 'code' in self.kwargs:
            code = get_object_or_404(ResetPasswordCode, code=self.kwargs['code'])
            return code.user.profile
        raise Http404
