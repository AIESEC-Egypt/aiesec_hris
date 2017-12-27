from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    TemplateView,
    FormView,
    UpdateView,
    DetailView)

from aiesec_hris.core.utility import Http401
from aiesec_hris.core.views.mixins import JsonFormInvalidMixin
from .forms import EventForm
from .models import Event


class EventList(LoginRequiredMixin, TemplateView):
    """
    Template view for calendar of events.
    Event instances are retrieved separtely via ajax
    Author: Nader Alexan
    """
    template_name = 'events/event_list.html'

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['form'] = EventForm()
        return context


def event_list_json(request):
    """
    List of events in Json format
    Author: Nader Alexan
    """
    if request.user.is_anonymous():
        return Http401()
    events = []
    for event in Event.objects.all():
        events.append({
            "id": event.id,
            "name": event.title,
            "startdate": event.start_date.strftime('%Y-%m-%d'),
            "enddate": event.end_date.strftime('%Y-%m-%d'),
            "starttime": event.start_time.strftime('%H:%M') if event.start_time else None,
            "endtime": event.end_time.strftime('%H:%M') if event.end_time else None,
            "notes": event.notes,
            "owner_id": event.owner.id
        })
    return JsonResponse({"monthly": events})


class EventCreate(LoginRequiredMixin, JsonFormInvalidMixin, FormView):
    """
    Event create view
    Author: Nader Alexan
    """
    form_class = EventForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        form.save_m2m()
        return JsonResponse(
            {'details': 'Event created successfully'}, status=201)


class EventUpdate(LoginRequiredMixin, JsonFormInvalidMixin, UpdateView):
    """
    Event update view
    Author: Nader Alexan
    """
    template_name = 'events/event_update.html'
    success_url = '/event/list/'
    form_class = EventForm

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)


def event_delete_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    title = event.title
    if event.owner == request.user:
        event.delete()
        success_message = 'event %s deleted successfully' % title
        messages.success(
            request, success_message)
        return JsonResponse(
            {'details': success_message})
    return JsonResponse(
        {'details': 'You do not have permission to delete this event'},
        status=401)


class EventDetail(LoginRequiredMixin, DetailView):
    """
    Event detail view
    Author: Nader Alexan
    """
    template_name = 'events/event_detail.html'
    model = Event
    fields = (
        'title',
        'start_date',
        'start_time',
        'end_date',
        'end_time',
        'notes',
        'invitees'
    )

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        return context
