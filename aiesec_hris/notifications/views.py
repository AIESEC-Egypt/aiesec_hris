# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView

from .models import Notification


class NotificationList(LoginRequiredMixin, ListView):
    """
    Notifications list view
    Author: Nader Alexan
    """
    template_name = 'notification_list.html'
    model = Notification

    def get_queryset(self):
        return self.model.objects.filter(receiver=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(NotificationList, self).get_context_data(**kwargs)
        object_list = context.get('object_list')
        unread = list(object_list.filter(read=False), )
        read = list(object_list.filter(read=True))
        context.update({
            'unread': unread,
            'read': read
        })
        object_list.update(read=True)
        return context


def notifications_count(request):
    """
    Unread notifications count
    Author: Nader Alexan
    """
    if request.user.is_anonymous:
        count = 0
    else:
        count = Notification.objects.filter(
            read=False, receiver=request.user).count()
    return JsonResponse(
        {'count': count})
