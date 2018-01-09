from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.TaskList.as_view(), name='task-list'),
    url(r'^create/$', views.TaskCreate.as_view(), name='task-create'),
    url(
        r'^detail/(?P<pk>\d+)/$',
        views.TaskDetail.as_view(),
        name='task-detail'),
    url(
        r'^delete/(?P<pk>\d+)/$',
        views.task_delete_view,
        name='task-delete'),
    url(
        r'^status/(?P<pk>\d+)/(?P<status>\w+)/$',
        views.TaskStatusUpdate.as_view(),
        name='task-status-update'),
    url(
        r'^submit/(?P<pk>\d+)/$',
        views.TaskSubmit.as_view(),
        name='task-submit'),
]
