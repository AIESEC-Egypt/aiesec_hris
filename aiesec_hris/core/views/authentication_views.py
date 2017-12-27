# Avoid importing settings directly to
# allow tests to use test-specific settings
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime

from ..forms import (
    ChangePasswordForm,
    ForgotPasswordForm,
    ResetPasswordForm)
from ..models import ResetPasswordCode
from .mixins import JsonFormInvalidMixin


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        """
        if user is Declined so he'll redirect to <success_url>
        :param request:
        :return:
        """
        login_message = "Email/Password Combination is incorrect"
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            profile = user.profile
            if profile.verification_issue == 4:
                login(request, user)
                return JsonResponse({"details": "Success"}, status=200)
            elif profile.verification_issue in [2, 3]:
                ResetPasswordCode.objects.filter(user=profile.user).delete()
                code_obj = ResetPasswordCode(user=profile.user)
                code_obj.save()
                profile_update_url = reverse('profile-update',
                                             kwargs={'code': code_obj.code})
                return JsonResponse({'details': """Your Account was declined
                 you'll redirect to edit page""",
                                     'success_url': '%s' % profile_update_url})
            elif profile.verification_issue == 1:
                login_message = "Your account has not been reviewed yet"
        return JsonResponse({
            "details": login_message}, status=401)

    def get(self, request):
        if not request.user.is_anonymous():
            return HttpResponseRedirect(reverse('post-list'))
        return super(LoginView, self).get(request)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


class ChangePasswordView(LoginRequiredMixin, JsonFormInvalidMixin, FormView):
    form_class = ChangePasswordForm
    template_name = 'change_password.html'

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get('new_password'))
        user.save()
        return JsonResponse({'details': 'Password changed successfully'})

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        Overriding the default to include request in order for the form
        to be able to get the current user
        Author: Nader Alexan
        """
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ForgotPasswordView(JsonFormInvalidMixin, FormView):
    form_class = ForgotPasswordForm
    template_name = 'forgot_password.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = get_object_or_404(User, email=email)
        ResetPasswordCode.objects.filter(user=user).delete()
        reset_password_code = ResetPasswordCode(user=user)
        reset_password_code.save()
        if not self.request.GET.get('testing'):
            domain = self.request.META['HTTP_HOST']
            message = """
            Hello,
            
            You have recently requested to reset your password.

            Please follow the link: %s/reset-password/%s

            If you did not request password reset, you can safely ignore this email

            Best regards,
            Jet8 Team
            """ % (
                domain,
                reset_password_code.code)
            send_mail(
                'Password Reset Link',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        return JsonResponse({
            'details': 'An email has been sent with a link to reset your password'})


class ResetPasswordView(JsonFormInvalidMixin, FormView):
    template_name = 'reset_password.html'
    form_class = ResetPasswordForm

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        password = form.cleaned_data.get('new_password')
        code = kwargs.get('code')
        reset_password_code = get_object_or_404(ResetPasswordCode, code=code)
        user = reset_password_code.user
        user.set_password(password)
        user.save()
        messages.success(
            self.request, 'Password changed successfully')
        return HttpResponseRedirect(reverse('login'))

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        reset_password_code = get_object_or_404(ResetPasswordCode, code=code)
        if (
                        datetime.datetime.now() - reset_password_code.created_at >
                    datetime.timedelta(minutes=5)):
            context = {
                'message': 'Reset password url expired, please request a new one and note that it is only valid for 5 minutes',
                'alert_type': 'danger'}
            self.template_name = 'message.html'
            return self.render_to_response(context)
        else:
            return self.render_to_response(self.get_context_data())
