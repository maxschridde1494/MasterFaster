from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
#from django.template import RequestContext
from sales.models import Sale, Product, ShoppingCartItems, Purchases
from sales.forms.forms import TestPaymentForm
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
from django.core.mail import send_mail, BadHeaderError

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
		context['quantity'] = int(request.POST['quantity'])
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
		success, instance = sale.charge(amount, request.POST['stripeToken'], u.email)
		if not success:
			return HttpResponse("Error reading card.")
		else:
			try:
				billing = Billing.objects.get(user=u)
			except Billing.DoesNotExist:
				billing = Billing(user=u)
			billing.address = request.POST['args[billing_address_line1]']
			billing.city = request.POST['args[billing_address_city]']
			billing.state = request.POST['args[billing_address_state]']
			billing.zipcode = request.POST['args[billing_address_zip]']
			billing.country = request.POST['args[billing_address_country]']
			billing.save()

			try:
				shipping = Shipping.objects.get(user=u)
			except Shipping.DoesNotExist:
				shipping = Shipping(user=u)

			shipping.address = request.POST['args[shipping_address_line1]']
			shipping.city = request.POST['args[shipping_address_city]']
			shipping.state = request.POST['args[shipping_address_state]']
			shipping.zipcode = request.POST['args[shipping_address_zip]']
			shipping.country = request.POST['args[shipping_address_country]']
			shipping.save()

			sale.date = timezone.now()
			sale.amount = amount
			sale.user = u
			sale.save()
			request.session['sale_id'] = sale.id

			#Send Confirmation email.
			subject = "Master Faster Confirmation Email."
			message = "Thank you for shopping with Master Faster. Your payment successfully went through. You will be receiving your receipt shortly."
			from_email = settings.EMAIL_HOST_USER
			to_email = request.POST.get('emailAddress', '')
			if subject and message and from_email:
				try:
					send_mail(subject, message, from_email, [to_email])
				except BadHeaderError:
					print("Email didn't go through")
			return HttpResponse('Successful Charge.')
	return HttpResponse("Invalid match.")

@login_required
def charge_confirmation(request, amount):
	if request.method == 'GET' and request.session.get('sale_id', None) != None:
		context = {'add': False}
		context['amount'] = cents_to_dollars(amount)
		#get purchase items for confirmation page
		sale_id = request.session.pop('sale_id', None)
		print('sale_id: ')
		print (request.session.get('sale_id', None))
		print(sale_id)
		if sale_id != None:
			sale = Sale.objects.get(pk=sale_id)
			context['conf_num'] = sale.charge_id
		user = User.objects.get(username=request.user)
		scart_items = ShoppingCartItems.objects.filter(user=user)
		purchases = {}
		for c_item in scart_items:
			p = Product.objects.get(pk=c_item.pid)
			purchases[(p.name, c_item.size)] = {'quantity': c_item.quantity, 'size': c_item.size, 'price': p.price}
			#save as purchase
			purchase = Purchases(user=user, sale_id=sale_id, pid=c_item.pid, pname=p.name, pprice=p.price, quantity=c_item.quantity, size=c_item.size)
			purchase.save()
			#delete all ShoppingCartItems related to user who just paid
			c_item.delete()
		context['purchases'] = purchases	
		print(Purchases.objects.all())	
		return HttpResponse(render(request, 'sales/confirmation.html', context))
	return HttpResponse('Fail')


@login_required
def checkout(request):
	if request.method == 'POST':
		pass
	else:
		user = User.objects.get(username=request.user)
		context = {}
		print('API KEYS:')
		print(settings.STRIPE_API_KEY_PUBLISHABLE, settings.STRIPE_API_KEY_SECRET)
		context = {'email': user.email, 'stripe_api_key': settings.STRIPE_API_KEY_PUBLISHABLE}
		context['img'] = gravatar(User.objects.get(username=request.user).email)
		products = ShoppingCartItems.objects.filter(user=user).order_by('-quantity')
		items = [{'product': Product.objects.get(pk=p.pid), 'cartItem': p} for p in products]
		context['items'] = items
		context['total_price_dollars'] = get_shopping_cart_total_price(user)
		context['amount'] = dollar_str_to_cents_int(context['total_price_dollars'])
		context['billing_bool'] = 'billing'
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
def purchase_history(request):
	if request.method == 'GET':
		u = User.objects.get(username=request.user)
		purchases = Purchases.objects.filter(user=u)
		context={'sales': {}}
		context['length'] = 0
		for purchase in purchases:
			if context['sales'].get(purchase.sale_id, None) == None:
				sale = Sale.objects.get(pk=purchase.sale_id)
				context['sales'][purchase.sale_id] = {'sale': sale,'amount':cents_to_dollars(sale.amount), 'products':[]}
				context['length'] += 1
			context['sales'][purchase.sale_id]['products'].append({'Product Name': purchase.pname, 'Price': purchase.pprice, \
				'Size': purchase.size,'Quantity': purchase.quantity})
		return HttpResponse(render(request, 'sales/purchasehistory.html', context))

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

           