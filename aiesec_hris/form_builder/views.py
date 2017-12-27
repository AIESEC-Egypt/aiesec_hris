from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    FormView
)

from aiesec_hris.core.views.mixins import PostFormAndFormsetInvalidMixin, JsonFormInvalidMixin
from .forms import QuestionForm, FormForm, SubmitFormForm
from .models import Form, SubmitForm, Answer

User = get_user_model()


class FormDetailView(DetailView):
    """
    Author : AmrAnwar
    """
    context_object_name = 'form'
    model = Form
    template_name = 'forms/form_detail.html'
    fields = ['title', 'share', 'external', 'created_at']
    question_fields = ['question', 'type', 'required', 'multiple', 'choices']

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(FormDetailView, self).get_context_data(**kwargs)
        context.update({
            'fields': self.fields,
            'question_fields': self.question_fields
        })
        return context


class FormListView(LoginRequiredMixin, ListView):
    """
    list of check user forms
    Author: AmrAnwar
    """
    context_object_name = 'forms'
    model = Form
    template_name = 'forms/forms_list.html'

    def get_queryset(self):
        """
        :return: filter forms by form owner user
        """
        return self.model.objects.filter(owner=self.request.user)


class FormCreateView(
    LoginRequiredMixin,
    PostFormAndFormsetInvalidMixin,
    FormView):
    """
    Form create view
    Author: Nader Alexan
    """
    template_name = 'forms/form_form.html'
    form_class = FormForm
    question_prefix = 'question'
    QuestionFormSet = formset_factory(QuestionForm)

    def get_context_data(self, **kwargs):
        context = {
            'form_form': FormForm(),
            'question_formset': self.QuestionFormSet(
                prefix=self.question_prefix)
        }
        return context

    def post(self, request, *args, **kwargs):
        question_formset = self.QuestionFormSet(
            request.POST, prefix=self.question_prefix)
        form_form = FormForm(request.POST)
        if form_form.is_valid() and question_formset.is_valid():
            return self.form_valid(form_form, question_formset)
        else:
            return self.form_invalid(form_form, question_formset)

    def form_valid(self, form, formset):
        _form = form.save(commit=False)
        _form.owner = self.request.user
        _form.save()
        for i, question_form in enumerate(formset):
            question = question_form.save(commit=False)
            question.form = _form
            question.order = i
            question.save()
        return JsonResponse({
            'details': 'Form created successfully',
            'success_url': _form.get_absolute_url()}, status=201)


def form_delete_view(request, pk):
    form = get_object_or_404(Form, pk=pk)
    title = form.title
    if form.owner == request.user:
        form.delete()
        success_message = 'form %s deleted successfully' % title
        messages.success(
            request, success_message)
        return JsonResponse(
            {'details': success_message})
    return JsonResponse(
        {'details': 'You do not have permission to delete this form'},
        status=401)


class SubmissionDetail(LoginRequiredMixin, DetailView):
    model = SubmitForm
    template_name = 'forms/submission_detail.html'
    fields = (
        'form',
        'user',
        'visitor',
        'visitor_email',
        'created_at')
    answer_fields = (
        'question',
        'value')

    def get_queryset(self):
        return SubmitForm.objects.filter(form__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SubmissionDetail, self).get_context_data(**kwargs)
        context.update({
            'fields': self.fields,
            'answer_fields': self.answer_fields
        })
        return context


class SubmissionCreate(DetailView):
    model = Form
    answer_prefix = 'answer'
    template_name = 'forms/submission_form.html'

    def get_formset(self):
        form = self.get_object()
        AnswerFormset = modelformset_factory(
            Answer,
            extra=form.question_form.count(),
            fields=['value'])
        formset = AnswerFormset(
            prefix=self.answer_prefix)
        data = {
            '%s-TOTAL_FORMS' % self.answer_prefix: form.question_form.count(),
            '%s-INITIAL_FORMS' % self.answer_prefix: '0',
            '%s-MAX_NUM_FORMS' % self.answer_prefix: '1000',
        }
        data.update(self.request.POST)
        formset = AnswerFormset(
            data,
            prefix=self.answer_prefix)
        return formset

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreate, self).get_context_data(**kwargs)
        form = self.get_object()
        context['formset'] = self.get_formset()
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous() and not kwargs.get('submit_form_pk'):
            return HttpResponseRedirect(reverse('submission-login', kwargs=kwargs))

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        answers_formset = self.get_formset()
        if answers_formset.is_valid():
            return self.form_valid(answers_formset, **kwargs)
        else:
            return self.form_invalid(answers_formset)

    def form_valid(self, formset, **kwargs):
        submit_form_pk = kwargs.get('submit_form_pk')
        if submit_form_pk:
            submit_form = SubmitForm.objects.get(pk=submit_form_pk)
        else:
            submit_form = SubmitForm(
                form=self.get_object(), user=self.request.user)
            submit_form.save()
        for answer_form, question in zip(formset, self.get_object().question_form.all()):
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()
            submit_form.answers.add(answer)
        submit_form.save()
        messages.success(self.request, 'Thank you for your submission')
        return JsonResponse({
            'details': 'Submission submitted successfully',
            'success_url': reverse('message-view')
        })

    def form_invalid(self, formset):
        def get_errors(form):
            errors = []
            for field in form:
                if field.errors:
                    errors.append("%s<br>%s" % (field.label, field.errors))
            return errors

        errors = []
        for f in formset:
            errors += get_errors(f)
        return JsonResponse({'details': errors}, status=400)


class SubmissionLogin(JsonFormInvalidMixin, DetailView):
    model = Form
    template_name = 'forms/submission_login.html'

    def get_context_data(self, **kwargs):
        context = super(SubmissionLogin, self).get_context_data(**kwargs)
        context['submit_form_form'] = SubmitFormForm()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated():
            return HttpResponseRedirect(
                reverse('submission-create', kwargs={'pk': self.object.pk}))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = SubmitFormForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        obj, created = SubmitForm.objects.get_or_create(
            form=self.get_object(),
            visitor_email=form.cleaned_data.get('visitor_email'),
            visitor=True)
        return JsonResponse({
            'details': 'Success',
            'success_url': reverse(
                'submission-create',
                kwargs={
                    'pk': obj.form.pk,
                    'submit_form_pk': obj.pk})})
