import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, FormView, DetailView

from aiesec_hris.core.views.mixins import JsonFormInvalidMixin
from .forms import TaskForm
from .models import Task


class TaskList(LoginRequiredMixin, TemplateView):
    """
    Lists new, submitted, accepted, and created by me tasks
    Author: Nader Alexan
    """
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context.update({
            'new_tasks': Task.objects.filter(
                assignee=self.request.user, status=1),
            'submitted_tasks': Task.objects.filter(
                assignee=self.request.user, status=2),
            'accepted_tasks': Task.objects.filter(
                assignee=self.request.user, status=3),
            'created_by_me_tasks': Task.objects.filter(
                assigner=self.request.user),
            'form': TaskForm()})
        return context


class TaskCreate(LoginRequiredMixin, JsonFormInvalidMixin, FormView):
    """
    Creates new task
    Author: Nader Alexan
    """
    template_name = 'tasks/task_list.html'
    form_class = TaskForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.assigner = self.request.user
        instance.save()
        return JsonResponse(
            {'details': 'Task created successfully'}, status=201)


class TaskDetailBase(LoginRequiredMixin, DetailView):
    """
    Base class for task detail
    Author: Nader Alexan
    """
    template_name = 'tasks/task_detail.html'
    model = Task

    def get_queryset(self):
        return self.model.objects.filter(
            Q(assignee=self.request.user) |
            Q(assigner=self.request.user))


class TaskDetail(TaskDetailBase):
    """
    Detail view for task
    Author: Nader Alexan
    """
    pass


class TaskStatusUpdate(TaskDetailBase):
    """
    Accepting/Rejecting a submitted task
    Author: Nader Alexan
    """

    def get_queryset(self):
        return self.model.objects.filter(
            assigner=self.request.user)

    def get(self, request, pk, status):
        self.object = self.get_object()
        if status == 'accept':
            self.object.status = 3
        elif status == 'reject':
            self.object.status = 4
        self.object.save()
        return HttpResponseRedirect(reverse('task-detail', kwargs={'pk': pk}))


class TaskSubmit(TaskDetailBase):
    """
    Submit a task
    Author: Nader Alexan
    """

    def get_queryset(self):
        return self.model.objects.filter(
            assignee=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.submission = request.POST.get('submission')
        self.object.status = 2
        self.object.submission_date = datetime.datetime.now()
        self.object.save()
        return HttpResponseRedirect(reverse('task-detail', kwargs=kwargs))


def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    title = task.title
    if request.user == task.assigner:
        task.delete()
        success_message = 'Task %s deleted successfully' % title
        messages.success(
            request, success_message)
        return JsonResponse(
            {'details': success_message})
    return JsonResponse(
        {'details': 'You do not have permission to delete this task'},
        status=401)
