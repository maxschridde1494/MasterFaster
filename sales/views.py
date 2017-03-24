from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
#from django.template import RequestContext
from sales.models import Sale
from masterfaster.models import User, CreditCard
from django.contrib.auth.decorators import login_required
from django import forms
from utils import gravatar
from django.conf import settings

@login_required
def charge(request):
	if request.method == "POST":
		u = User.objects.get(username=request.user)
		credit_card = CreditCard.objects.get(user=u)
		sale = Sale()
		print(request.POST)
		#pass in CHECKOUT token
		success, instance = sale.charge(100, request.POST['stripeToken'])
		if not success:
			return HttpResponse(render(request, 'sales/charge.html', {'errors': "Charge didn't go through because " + instance.json_body['error']['message']}))
		else:
			instance.save()
			print("Success! We've charged your card!")
			return redirect('sales:charge')

	else:
		user = User.objects.get(username=request.user)
		img = gravatar(user.email)
		context = {
			'img': img,
			'email': user.email,
			'amount': 1000,
			'stripe_api_key': settings.STRIPE_API_KEY_PUBLISHABLE,
		}
		return HttpResponse(render(request, 'sales/charge.html', context))


            