from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name='blog'
urlpatterns = [
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.blogfeed_month, name='blogfeed_month'),
    url(r'^$', views.blogfeed, name='feed'),
    url(r'^(?P<entry_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<entry_id>[0-9]+)/comment/$', views.comment, name='comment'),
]