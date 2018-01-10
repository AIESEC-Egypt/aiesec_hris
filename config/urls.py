from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView

from aiesec_hris.core import views

urlpatterns = [
                  url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
                  url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

                  # Django Admin, use {% url 'admin:index' %}
                  url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
                  url(settings.ADMIN_URL, admin.site.urls),

                  # User management
                  url(r'^users/', include('aiesec_hris.users.urls', namespace='users')),
                  url(r'^accounts/', include('allauth.urls')),

                  url(r'^comments/', include('aiesec_hris.comments.urls')),
                  url(r'^education/', include('aiesec_hris.education.urls')),

                  url(r'^$', views.IndexView.as_view(), name='index'),

                  # Accounts urls
                  url(
                      r'^accounts/register/$',
                      views.RegisterView.as_view(),
                      name='register'),
                  url(
                      r'^accounts/update/(?P<code>.+)/$',
                      views.ProfileDeclineUpdate.as_view(),
                      name='profile-update'
                  ),
                  # Authentication urls
                  url(r'^auth/login/$', views.LoginView.as_view(), name='login'),
                  url(r'^auth/logout/$', views.LogoutView.as_view(), name='logout'),
                  url(
                      r'^auth/change-password/$',
                      views.ChangePasswordView.as_view(),
                      name='change-password'),
                  url(
                      r'^reset-password/(?P<code>.+)/$',
                      views.ResetPasswordView.as_view(),
                      name='reset-password'),
                  url(
                      r'^forgot-password/$',
                      views.ForgotPasswordView.as_view(),
                      name='forgot-password'),

                  # Forms url
                  url(r'^forms/', include('aiesec_hris.form_builder.urls')),

                  url(
                      r'^experience_points/update/(?P<pk>\d+)/$',
                      views.ExperiencePointsUpdate.as_view(),
                      name='experience-points-update'),

                  # Events urls
                  url(r'^event/', include('aiesec_hris.events.urls')),

                  # Stats urls
                  url(
                      r'^stats/$',
                      views.StatsView.as_view(),
                      name='stats'),

                  # HR urls
                  url(r'^lc/list/$', views.LCList.as_view(), name='lc-list'),
                  url(r'^lc/(?P<pk>\d+)/$', views.LCDetail.as_view(), name='lc-detail'),

                  # message urls
                  url(r'^message/$', views.MessageView.as_view(), name='message-view'),

                  # Tasks urls
                  url(r'^task/', include('aiesec_hris.tasks.urls')),

                  # Notification urls
                  url(r'^notification/', include('aiesec_hris.notifications.urls')),

                  # position urls
                  url(r'^positions/(?P<pk>\d+)/$', views.positions_json, name='positions'),

                  # account moderation urls
                  url(r'^moderation/$', views.reviews_list, name="moderation-list"),
                  url(r'^moderation/(?P<id>\d+)/accept/$', views.profile_accept,
                      name="moderation-accept"),
                  url(r'moderation/(?P<id>\d+)/decline$', views.profile_decline,
                      name="moderation-decline"),

                  # Profile urls
                  url(
                      r'^profile/(?P<pk>\d+)/$',
                      views.ProfileDetail.as_view(),
                      name='profile-detail'),
                  url(
                      r'^profile/update/(?P<pk>\d+)/$',
                      views.ProfileUpdate.as_view(),
                      name='profile-update'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
                          url(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
