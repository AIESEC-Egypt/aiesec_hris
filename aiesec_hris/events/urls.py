from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.EventList.as_view(), name='event-list'),
    url(r'^list/json/$', views.event_list_json, name='event-list-json'),
    url(r'^create/$', views.EventCreate.as_view(), name='event-create'),
    url(
        r'^(?P<pk>\d+)/$',
        views.EventDetail.as_view(),
        name='event-detail'),
    url(
        r'^update/(?P<pk>\d+)/$',
        views.EventUpdate.as_view(),
        name='event-update'),
    url(
        r'^delete/(?P<pk>\d+)/$',
        views.event_delete_view,
        name='event-delete'),
]
