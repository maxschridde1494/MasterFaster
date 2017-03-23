from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name='blog'
urlpatterns = [
    url(r'^feed/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.blogfeed_month, name='blogfeed_month'),
    url(r'^feed/$', views.blogfeed, name='feed'),
    url(r'^(?P<entry_id>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^new_entry/$', views.newEntry, name='newEntry'),
    url(r'^(?P<entry_id>[0-9]+)/comment/$', views.comment, name='comment'),
]