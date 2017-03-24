from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
#from django.template import RequestContext
from sales.models import Sale
from masterfaster.models import User, CreditCard
from django.contrib.auth.decorators import login_required
from django import forms
from utils import gravatar

@login_required
def charge(request):
	if request.method == "POST":
		u = User.objects.get(username=request.user)
		credit_card = CreditCard.objects.get(user=u)
		sale = Sale()
		#test with $10.00 charge for now
		success, instance = sale.charge(1000, credit_card.number, credit_card.exp_date_month, credit_card.exp_date_year, credit_card.csv)
		if not success:
			return HttpResponse(render(request, 'sales/charge.html', {'errors': "Charge didn't go through because " + instance.json_body['error']['message']}))
		else:
			instance.save()
			return HttpResponse("Success! We've charged your card!")
	else:
		user = User.objects.get(username=request.user)
		img = gravatar(user.email)
		context = {
			'img': img
		}
		return HttpResponse(render(request, 'sales/charge.html', context))


            