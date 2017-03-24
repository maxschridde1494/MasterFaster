from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name='sales'
urlpatterns = [
    url(r'^charge/$', views.charge, name='charge'),
]