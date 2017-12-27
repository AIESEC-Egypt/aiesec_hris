from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.FormListView.as_view(),
        name='form-list'),
    url(
        r'^create/$',
        views.FormCreateView.as_view(),
        name='form-create'),
    url(
        r'^(?P<pk>\d+)/$',
        views.FormDetailView.as_view(),
        name='forms-detail'),
    url(
        r'^delete/(?P<pk>\d+)/$',
        views.form_delete_view,
        name='form-delete'),
    url(
        r'^submission/(?P<pk>\d+)/$',
        views.SubmissionDetail.as_view(),
        name='submission-detail'),
    url(
        r'^(?P<pk>\d+)/submission/login/$',
        views.SubmissionLogin.as_view(),
        name='submission-login'),
    url(
        r'^(?P<pk>\d+)/submission/create/$',
        views.SubmissionCreate.as_view(),
        name='submission-create'),
    url(
        r'^(?P<pk>\d+)/submission/create/(?:(?P<submit_form_pk>\d+))$',
        views.SubmissionCreate.as_view(),
        name='submission-create'),

]
