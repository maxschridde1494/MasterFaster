from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
#from django.template import RequestContext
from sales.models import Sale, Product, ShoppingCartItems
from .forms.forms import TestPaymentForm
from masterfaster.models import User, CreditCard, Shipping, Billing
from masterfaster.forms.forms import EditShippingAddress, EditBillingAddress
from django.contrib.auth.decorators import login_required
from django import forms
from utils import gravatar, dollar_str_to_cents_int, cents_to_dollars, get_shopping_cart_total_price, address_empty
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
		except ShoppingCartItems.DoesNotExist:
			scart_item = ShoppingCartItems(user=user,pid=product_id,quantity=quantity,size=size)
		scart_item.save()
		
		context = {}
		context['product_name'] = Product.objects.get(pk=product_id).name
		context['quantity'] = request.POST['quantity']
		context['add'] = True
		return HttpResponse(render(request, 'sales/confirmation.html', context))

	return redirect(reverse('sales:itemDetail', args=[product_id]))

@login_required
def charge(request, amount):
	if request.method == 'POST':
		if amount == '0':
			return redirect('sales:checkout')
		u = User.objects.get(username=request.user)
		sale = Sale()
		#stripe charge
		success, instance = sale.charge(amount, request.POST['stripeToken'])
		if not success:
			return HttpResponse("Error reading card.")
		else:
			sale.date = timezone.now()
			sale.amount = amount
			sale.user = u
			sale.save()
			request.session['sale_id'] = sale.id
			return HttpResponse('Successful Charge.')
	return HttpResponse("Invalid match.")

@login_required
def charge_confirmation(request, amount):
	if request.method == 'GET':
		context = {'add': False}
		context['amount'] = cents_to_dollars(amount)
		#get purchase items for confirmation page
		sale_id = request.session.pop('sale_id', None)
		if sale_id != None:
			sale = Sale.objects.get(pk=sale_id)
			context['conf_num'] = sale.charge_id
		scart_items = ShoppingCartItems.objects.filter(user=User.objects.get(username=request.user))
		purchases = {}
		for c_item in scart_items:
			p = Product.objects.get(pk=c_item.pid)
			purchases[(p.name, c_item.size)] = {'quantity': c_item.quantity, 'size': c_item.size, 'price': p.price}
		context['purchases'] = purchases
		#delete all ShoppingCartItems related to user who just paid
		for item in scart_items:
			item.delete()
		print('charge_confirmation context: ')
		print(context)
		return HttpResponse(render(request, 'sales/confirmation.html', context))
	return HttpResponse('Fail')


@login_required
def checkout(request):
	if request.method == 'POST':
		pass
	else:
		user = User.objects.get(username=request.user)
		context = {}
		# context = {'email': user.email, 'stripe_api_key': settings.STRIPE_API_KEY_PUBLISHABLE}
		# context['img'] = gravatar(User.objects.get(username=request.user).email)
		products = ShoppingCartItems.objects.filter(user=user).order_by('-quantity') 
		items = [(Product.objects.get(pk=p.pid),p) for p in products]
		context['items'] = items
		# if items:
		# 	prices = [item[1].quantity*item[0].price for item in items]
		# 	total_price = functools.reduce(lambda x,y: x+y, prices, 0)
		# else:
		# 	total_price = 0.00
		context['total_price_dollars'] = get_shopping_cart_total_price(user)
		context['amount'] = dollar_str_to_cents_int(context['total_price_dollars'])
		context['billing_bool'] = 'billing'
		# try:
		# 	shippingForm = EditShippingAddress(instance=Shipping.objects.get(user=user))
		# except Shipping.DoesNotExist:
		# 	shippingForm = EditShippingAddress()
		# context['shipping'] = shippingForm
		return HttpResponse(render(request, 'sales/shoppingcart.html', context))

@login_required
def edit_addresses(request, billing_bool):
	user = User.objects.get(username=request.user)
	context = {'email': user.email, 'stripe_api_key': settings.STRIPE_API_KEY_PUBLISHABLE}
	context['img'] = gravatar(User.objects.get(username=request.user).email)
	if request.method == 'POST':
		if billing_bool == 'billing':
			billingForm = EditBillingAddress(request.POST)
			if billingForm.is_valid():
				#save edited billing information
				try:
					billing = Billing.objects.get(user=user)
				except Billing.DoesNotExist:
					billing = Billing(user=user)
				billing.address = billingForm.cleaned_data['address']
				billing.city = billingForm.cleaned_data['city']
				billing.state = billingForm.cleaned_data['state']
				billing.zipcode = billingForm.cleaned_data['zipcode']
				billing.country = billingForm.cleaned_data['country']
				billing.save()
				try:
					shipping = Shipping.objects.get(user=user)
				except Shipping.DoesNotExist:
					shipping = Shipping(user=user)
				if shipping.same_as_billing:
					shipping.address = billing.address
					shipping.city = billing.city
					shipping.state = billing.state
					shipping.zipcode = billing.zipcode
					shipping.country = billing.country	
					shipping.same_as_billing = True	
					shipping.save()
			return redirect(reverse('sales:editAddresses', args=['billing']))

		else:
			shippingForm = EditShippingAddress(request.POST)
			if shippingForm.is_valid():
				#save edited shipping information
				try:
					shipping = Shipping.objects.get(user=user)
				except Billing.DoesNotExist:
					shipping = Shipping(user=user)
				if shippingForm.cleaned_data['same_as_billing'] == True:
					try:
						billing = Billing.objects.get(user=user)
					except Billing.DoesNotExist:
						billing = Billing(user=user)
					shipping.address = billing.address
					shipping.city = billing.city
					shipping.state = billing.state
					shipping.zipcode = billing.zipcode
					shipping.country = billing.country	
					shipping.same_as_billing = True		
				else:
					shipping.address = shippingForm.cleaned_data['address']
					shipping.city = shippingForm.cleaned_data['city']
					shipping.state = shippingForm.cleaned_data['state']
					shipping.zipcode = shippingForm.cleaned_data['zipcode']
					shipping.country = shippingForm.cleaned_data['country']	
					shipping.same_as_billing = False		
				shipping.save()
				print('shipping same as billing after save %s' % str(shipping.same_as_billing))
			return redirect(reverse('sales:editAddresses', args=['shipping']))
	else:
		user = User.objects.get(username=request.user)
		try:
			billing = Billing.objects.get(user=user)
			billingForm = EditBillingAddress(instance=billing)
		except Billing.DoesNotExist:
			billing = Billing(user=user)
			billingForm = EditBillingAddress()
		try:
			shipping = Shipping.objects.get(user=user)
			shippingForm = EditShippingAddress(instance=shipping)
		except Shipping.DoesNotExist:
			shipping = Shipping(user=user)
			shippingForm = EditShippingAddress()
		if billing_bool == 'billing':
			context['address_form'] = billingForm
			context['edit_billing'] = True
		else:
			context['address_form'] = shippingForm
			context['edit_billing'] = False
		context['shipping_bool'] = 'shipping'
		context['billing_bool'] = 'billing'
		if not address_empty(shipping) and not address_empty(billing):
			context['both_addresses'] = True
			context['total_price_dollars'] = get_shopping_cart_total_price(user)
			context['amount'] = dollar_str_to_cents_int(context['total_price_dollars'])

		return HttpResponse(render(request, 'sales/payment.html', context))



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
	print('in home')
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
	cart_item.delete()
	return redirect('sales:checkout')

           