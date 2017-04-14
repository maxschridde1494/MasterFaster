from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name='sales'
urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^charge/(?P<amount>[0-9]+)/$', views.charge, name='charge'),
    url(r'^charge_confirmation/(?P<amount>[0-9]+)/$', views.charge_confirmation, name='chargeConfirmation'),
	url(r'^item/(?P<product_id>[0-9]+)/$', views.item_detail, name='itemDetail'),
	url(r'^add_to_cart/(?P<product_id>[0-9]+)/$', views.add_to_cart, name='addToCart'),
	url(r'^shopping_cart/$', views.checkout, name='checkout'),
	url(r'^shopping_cart/edit/(?P<cart_id>[0-9]+)/$', views.edit_cart_item, name='editCartItem'),
	url(r'^shopping_cart/remove/(?P<cart_id>[0-9]+)/$', views.remove_cart_item, name='removeCartItem'),
	url(r'^purchase_history/$', views.purchase_history, name='purchaseHistory')
]