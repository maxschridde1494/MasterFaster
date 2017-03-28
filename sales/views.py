from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
#from django.template import RequestContext
from sales.models import Sale, Product, ShoppingCartItems
from .forms.forms import TestPaymentForm
from masterfaster.models import User, CreditCard
from django.contrib.auth.decorators import login_required
from django import forms
from utils import gravatar, dollar_str_to_cents_int
from django.conf import settings
from django.utils import timezone
import functools
from django.urls import reverse
from django.contrib.sessions.models import Session

@login_required
def add_to_cart(request, product_id):
	user = User.objects.get(username=request.user)
	if request.method == 'POST':
		quantity, size = request.POST['quantity'], request.POST['size']
		try:
			#update if user already has same cart_item with same pid and size
			scart_item = ShoppingCartItems.objects.get(user=user,pid=product_id,size=size)
			scart_item.quantity += int(quantity)
			print('update')
		except ShoppingCartItems.DoesNotExist:
			scart_item = ShoppingCartItems(user=user,pid=product_id,quantity=quantity,size=size)
			print('new item')
		scart_item.save()
		print(scart_item.id)
		
		context = {}
		context['product_name'] = Product.objects.get(pk=product_id).name
		context['quantity'] = request.POST['quantity']
		return HttpResponse(render(request, 'sales/addconfirmation.html', context))

	return redirect(reverse('sales:itemDetail', args=[product_id]))

@login_required
def charge(request, amount):
	#PASS IN SHOPPING CART USER FOR VERIFICATION
	if request.method == 'POST':
		u = User.objects.get(username=request.user)
		sale = Sale()
		#stripe charge
		success, instance = sale.charge(amount, request.POST['stripeToken'])
		if not success:
			return HttpResponse(render(request, 'sales/addconfirmation.html'))
		else:
			sale.date = timezone.now()
			sale.amount = amount
			sale.user = u
			sale.save()
			#delete all ShoppingCartItems related to user who just paid
			scart_items = ShoppingCartItems.objects.filter(user=u)
			for item in scart_items:
				item.delete()
			print("Success! We've charged your card!")
			return redirect('sales:home')
	return HttpResponse("Invalid match.")

@login_required
def checkout(request):
	if request.method == 'POST':
		pass
	else:
		user = User.objects.get(username=request.user)
		context = {'email': user.email, 'stripe_api_key': settings.STRIPE_API_KEY_PUBLISHABLE}
		context['img'] = gravatar(User.objects.get(username=request.user).email)
		products = ShoppingCartItems.objects.filter(user=user).order_by('-quantity') 
		items = [(Product.objects.get(pk=p.pid),p) for p in products]
		context['items'] = items
		if items:
			prices = [item[1].quantity*item[0].price for item in items]
			total_price = functools.reduce(lambda x,y: x+y, prices, 0)
		else:
			total_price = 0.00
		context['total_price_dollars'] = total_price
		context['amount'] = dollar_str_to_cents_int(total_price)
		return HttpResponse(render(request, 'sales/shoppingcart.html', context))

@login_required
def edit_cart_item(request, cart_id):
	if request.method == 'POST':
		user = User.objects.get(username=request.user)
		quantity, size = request.POST['quantity'], request.POST['size']
		scart_item = ShoppingCartItems.objects.get(pk=cart_id)
		print(scart_item.id)
		scart_item.quantity = quantity
		scart_item.size = size
		scart_item.save()
		return redirect('sales:checkout')
	else:
		cart_item = ShoppingCartItems.objects.get(pk=cart_id)
		try:
			product = Product.objects.get(pk=cart_item.pid)
		except Product.DoesNotExist:
			pass
			#do something here
		context = {'product':product, 'cart_item_id': cart_id}
		return HttpResponse(render(request, 'sales/editcartitem.html', context))



def home(request):
	if request.method == 'POST':
		pass
	else:
		context = {}
		product_list = Product.objects.all()
		context['product_list'] = product_list
		if request.user.is_authenticated:
			context['img'] = gravatar(User.objects.get(username=request.user).email)
		return HttpResponse(render(request, 'sales/shopfeed.html', context))

@login_required
def item_detail(request, product_id):
	if request.method == 'POST':
		pass
	else:
		user = User.objects.get(username=request.user)
		try:
			product = Product.objects.get(pk=product_id)
		except:
			return HttpResponse(render(request, 'sales/shopitem.html'))
		context = {}
		context['product'] = product
		return HttpResponse(render(request, 'sales/shopitem.html', context))

@login_required
def remove_cart_item(request, cart_id):
	# user = User.objects.get(username=request.user)
	print(cart_id)
	try:
		cart_item = ShoppingCartItems.objects.get(pk=cart_id)
	except ShoppingCartItems.DoesNotExist:
		pass
		#figure out what to do if item doesn't exist

	#combine all cart items in shopping cart, so need to get all cart_items with same size and pid
	cart_item.delete()
	return redirect('sales:checkout')

           