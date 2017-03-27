from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name='sales'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^item/(?P<product_id>[0-9]+)/$', views.item_detail, name='itemDetail'),
    # url(r'^charge/(?P<product_id>[0-9]+)/$', views.charge, name='charge'),
]