from django.conf.urls import url

from aiesec_hris.education import views

urlpatterns = [

    url(
        r'^post/update/(?P<pk>\d+)/$',
        views.PostUpdate.as_view(),
        name='post-update'),
    url(
        r'^post/delete/(?P<pk>\d+)/$',
        views.post_delete_view,
        name='post-delete'),
    url(r'^post/create/$', views.PostCreate.as_view(), name='post-create'),
    url(r'^post/list/$', views.PostList.as_view(), name='post-list'),
    url(
        r'^post/(?P<pk>\d+)/$',
        views.PostDetail.as_view(),
        name='post-detail'),

]
