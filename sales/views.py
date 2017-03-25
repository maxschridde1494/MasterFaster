from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
#from django.template import RequestContext
from sales.models import Sale, Product
from .forms.forms import TestPaymentForm
from masterfaster.models import User, CreditCard
from django.contrib.auth.decorators import login_required
from django import forms
from utils import gravatar, dollar_str_to_cents_int
from django.conf import settings
from django.utils import timezone

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
		# HERE, RETRIEVE PRICE OF PRODUCT BEING CHARGED FOR
		try:
			product = Product.objects.get(pk=product_id)
		except:
			return HttpResponse(render(request, 'sales/shopitem.html'))
		u = User.objects.get(username=request.user)
		sale = Sale()
		#stripe charge
		success, instance = sale.charge(dollar_str_to_cents_int(product.price), request.POST['stripeToken'])
		if not success:
			return HttpResponse(render(request, 'sales/shopitem.html', {'product': product, 'errors': "Charge didn't go through because " + instance.json_body['error']['message']}))
		else:
			sale.date = timezone.now()
			sale.amount = product.price
			sale.user = u
			sale.save()
			print("Success! We've charged your card!")
			return redirect('sales:home')
	else:
		user = User.objects.get(username=request.user)
		context = {'email': user.email, 'stripe_api_key': settings.STRIPE_API_KEY_PUBLISHABLE}
		try:
			product = Product.objects.get(pk=product_id)
		except:
			return HttpResponse(render(request, 'sales/shopitem.html'))
		context['product'] = product
		context['amount'] = dollar_str_to_cents_int(product.price)
		return HttpResponse(render(request, 'sales/shopitem.html', context))

@login_required
def charge(request, product_id):
	if request.method == "POST":
		# HERE, RETRIEVE PRICE OF PRODUCT BEING CHARGED FOR
		if product_id == 4:
			amount = 400
			print('product id works')
		else:
			amount = 84
		u = User.objects.get(username=request.user)
		credit_card = CreditCard.objects.get(user=u)
		sale = Sale()
		#pass in CHECKOUT token
		success, instance = sale.charge(amount, request.POST['stripeToken'])
		if not success:
			return HttpResponse(render(request, 'sales/charge.html', {'errors': "Charge didn't go through because " + instance.json_body['error']['message']}))
		else:
			sale.date = timezone.now()
			sale.amount = '100'
			sale.user = u
			sale.save()
			print("Success! We've charged your card!")
			return redirect('sales:home')

	else:
		print("this is the product_id: %s" % product_id)
		user = User.objects.get(username=request.user)
		img = gravatar(user.email)
		context = {
			'img': img,
			'email': user.email,
			'amount': dollar_str_to_cents_int(request.GET['price']),
			'stripe_api_key': settings.STRIPE_API_KEY_PUBLISHABLE,
			'product_id': product_id,
		}
		return redirect('sales:charge product_id', context)
		# return HttpResponse(render(request, 'sales/charge.html', context))


            