from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
#from django.template import RequestContext
from sales.models import Sale
# from sales.forms.forms import SalePaymentForm
from django import forms
 
def charge(request):
# 	if request.method == "POST":
# 		form = SalePaymentForm(request.POST)
# 		if form.is_valid(): # charges the card
# 			number = form.cleaned_data["number"]
# 			exp_month = form.cleaned_data["expiration_month"]
# 			exp_year = form.cleaned_data["expiration_year"]
# 			cvc = form.cleaned_data["cvc"]

# 			sale = Sale()
# 			#NEED TO FIGURE OUT HOW TO PASS IN AMOUNT TO BE CHARGED
# 			success, instance = sale.charge(1000, number, exp_month, exp_year, cvc)
# 			if not success:
# 				return HttpResponse(render(request, 'sales/charge.html', {'form': form, 'errors': "Charge didn't go through because " + instance.json_body['error']['message']}))
# 				# raise forms.ValidationError("Error: %s" % instance.json_body['error']['message'])
# 			else:
# 				instance.save()
# 				# we were successful! do whatever you will here...
# 				# perhaps you'd like to send an email...
# 				pass
# 				return HttpResponse("Success! We've charged your card!")
# 	else:
# 		form = SalePaymentForm()
	return HttpResponse(render(request, 'sales/charge.html', {'form': form, 'errors': form.errors}))


            