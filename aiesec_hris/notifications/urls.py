from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^list/$',
        views.NotificationList.as_view(),
        name='notification-list'),
    url(
        r'^count/$',
        views.notifications_count,
        name='notification-count'),
]
