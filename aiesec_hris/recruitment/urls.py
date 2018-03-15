from django.conf.urls import url

from . import views

app_name = 'recruitment'

urlpatterns = [
    url(
        r'^register/$',
        views.register,
        name='member-registration'),
    url(
        r'^complete/$',
        views.registration_complete,
        name='registration-complete'),
    url(
        r'^list/$',
        views.recruitment_list,
        name='recruitment-list'),
    url(
        r'^profile/(?P<applicant_id>[0-9]+)/contact/',
        views.applicant_contacted,
        name='contact'),
    url(
        r'^profile/(?P<applicant_id>[0-9]+)/',
        views.applicant_profile,
        name='applicant-profile'),

]
