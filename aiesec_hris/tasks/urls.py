from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^task/list/$', views.TaskList.as_view(), name='task-list'),
    url(r'^task/create/$', views.TaskCreate.as_view(), name='task-create'),
    url(
        r'^task/detail/(?P<pk>\d+)/$',
        views.TaskDetail.as_view(),
        name='task-detail'),
    url(
        r'^task/delete/(?P<pk>\d+)/$',
        views.task_delete_view,
        name='task-delete'),
    url(
        r'^task/status/(?P<pk>\d+)/(?P<status>\w+)/$',
        views.TaskStatusUpdate.as_view(),
        name='task-status-update'),
    url(
        r'^task/submit/(?P<pk>\d+)/$',
        views.TaskSubmit.as_view(),
        name='task-submit'),
]
