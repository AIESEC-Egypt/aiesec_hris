from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^register/$',
        views.register,
        name='member-registration'),
    url(
        r'^complete/$',
        views.registration_complete,
        name='registration-complete'),
]
