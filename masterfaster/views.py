from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone
import datetime

from django.contrib.sessions.models import Session
from .models import User, Billing, Shipping
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms.forms import EditUserInfo, EditShippingAddress, EditBillingAddress, CreateUserForm
from utils import gravatar
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
	context = {}
	try:
		u = User.objects.get(username=request.user)
	except User.DoesNotExist:
		return HttpResponse(render(request, 'masterfaster/home.html', context))
	img = gravatar(u.email, 40)
	context['img'] = img
	return HttpResponse(render(request, 'masterfaster/home.html', context))

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			return redirect('masterfaster:editProfile')
		else:
			print('not valid form')
			print(form.errors)
			user = User.objects.get(username=request.user)
			img = gravatar(user.email)
			context = {
				'form': PasswordChangeForm(request.user),
				'img': img,
				'errors': form.errors
			}
			return HttpResponse(render(request, 'registration/password_change_form.html', context))
	else:
		user = User.objects.get(username=request.user)
		img = gravatar(user.email)
		form = PasswordChangeForm(request.user)
		context = {
			'form': form,
			'img': img
		}
		return HttpResponse(render(request, 'registration/password_change_form.html', context))

def createUser(request):
	if request.method == 'POST':
		#create a new user
		usernames = [u.username for u in User.objects.all()]
		uname = request.POST['username']
		if uname in usernames:
			#re-serve login page with message saying username is already taken
			context = {
				'creating_user': True,
				'taken_username': True,
				'creating_user_form': CreateUserForm()
			}
			return HttpResponse(render(request, 'registration/login.html', context))
		else:
		#NEED TO FIGURE OUT WHY form.is_valid() RETURNS FALSE 
			form = CreateUserForm(request.POST)
			print('checking form.is_valid')
			if form.is_valid():
				print('form.is_valid')
				password = form.cleaned_data['password']
				if password != form.cleaned_data['password2']:
					context = {
						'creating_user': True,
						'taken_username': False,
						'creating_user_form': CreateUserForm(),
						'not_matching_password': True
					}
					return HttpResponse(render(request, 'registration/login.html', context))
				elif len(password) < 8:
					context = {
						'creating_user': True,
						'taken_username': False,
						'creating_user_form': CreateUserForm(),
						'short_password': True
					}
					return HttpResponse(render(request, 'registration/login.html', context))
				email = form.cleaned_data['email']
				user = User.objects.create_user(uname, email, password)
				user.save()
				#automatically create billing address
				billing = Billing(user=user)
				billing.save()
				shipping = Shipping(user=user)
				shipping.save()
				print ('SAVING USER')
				u = authenticate(username=uname, password=password)
				#authenticate new user
				if u is not None:
					login(request, u)
					return redirect('masterfaster:home')
				else:
					#CHANGE THIS TO INVALID LOGIN PAGE
					context = {
						'creating_user': True,
						'taken_username': True,
						'creating_user_form': CreateUserForm()
					}
					return HttpResponse(render(request, 'registration/login.html', context))
			else:
				context = {
					'creating_user': True,
					'taken_username': False,
					'incorrect_email': True,
					'creating_user_form': CreateUserForm(),
					'errors': True
				}
				return HttpResponse(render(request, 'registration/login.html', context))
	else:
		context = {
			'creating_user': True,
			'taken_username': False,
			'creating_user_form': CreateUserForm()
		}
		return HttpResponse(render(request, 'registration/login.html', context))

@login_required
def editProfile(request):
	print('in edit profile')
	if request.method == 'POST':
		form = EditUserInfo(request.POST)
		if form.is_valid():
			user = User.objects.get(username=request.user)
			#post new profile information and save to db
			email = form.cleaned_data['email']
			ccn = form.cleaned_data['credit_card_number']
			cce = form.cleaned_data['credit_card_exp_date']
			ccc = form.cleaned_data['credit_card_csv']
			user.email = email
			user.credit_card_number = ccn
			user.credit_card_exp_date = cce
			user.credit_card_csv = ccc
			user.save()
			return redirect('masterfaster:editProfile')
	else:
		#load Edit Profile Template
		user = User.objects.get(username=request.user)
		img = gravatar(user.email)
		profile_form = EditUserInfo(instance=user)
		context = {
			'profile_form': profile_form,
			'edit_profile': True,
			'edit_shipping': False,
			'edit_billing': False,
			'img': img
		}
		return HttpResponse(render(request, 'masterfaster/editprofile.html', context))

@login_required
def editBillingAddress(request):
	print('in edit Address')
	if request.method == 'POST':
		form = EditBillingAddress(request.POST)
		if form.is_valid():
			user = User.objects.get(username=request.user)
			try:
				billing = Billing.objects.get(user=user)
			except Billing.DoesNotExist:
				billing = Billing(user=user)
			#save edited billing information
			billing.address = form.cleaned_data['address']
			billing.city = form.cleaned_data['city']
			billing.state = form.cleaned_data['state']
			billing.zipcode = form.cleaned_data['zipcode']
			billing.country = form.cleaned_data['country']			
			billing.save()
			return redirect('masterfaster:editBillingAddress')
	else:
		u = User.objects.get(username=request.user)
		img = gravatar(u.email)
		try:
			billing = Billing.objects.get(user=u)
		except Billing.DoesNotExist:
			billing = None
		if billing != None:
			billing_address_form = EditBillingAddress(instance=billing)
		else:
			billing_address_form = EditBillingAddress()
		context = {
			'address_form': billing_address_form,
			'edit_profile': False,
			'edit_billing': True,
			'edit_shipping': False,
			'img': img
		}
		return HttpResponse(render(request, 'masterfaster/editprofile.html', context))

@login_required
def editShippingAddress(request):
	if request.method == 'POST':
		form = EditShippingAddress(request.POST)
		if form.is_valid():
			user = User.objects.get(username=request.user)
			try:
				shipping = Shipping.objects.get(user=user)
			except Shipping.DoesNotExist:
				shipping = Shipping(user=user)
			#save edited billing information
			['address', 'city', 'state', 'zipcode', 'country', 'same_as_billing']
			if form.cleaned_data['same_as_billing'] == True:
				try:
					billing = Billing.objects.get(user=user)
				except Billing.DoesNotExist:
					shipping_address_form = EditShippingAddress(instance=shipping)
					context = {
						'address_form': shipping_address_form,
						'edit_profile': False,
						'edit_billing': False,
						'edit_shipping': True,
						'no_billing': True
					}
					return HttpResponse(render(request, 'masterfaster/editprofile.html', context))
				shipping.address = billing.address
				shipping.city = billing.city
				shipping.state = billing.state
				shipping.zipcode = billing.zipcode
				shipping.country = billing.country	
				shipping.same_as_billing = form.cleaned_data['same_as_billing']		
				shipping.save()
			else:		
				shipping.address = form.cleaned_data['address']
				shipping.city = form.cleaned_data['city']
				shipping.state = form.cleaned_data['state']
				shipping.zipcode = form.cleaned_data['zipcode']
				shipping.country = form.cleaned_data['country']	
				shipping.same_as_billing = form.cleaned_data['same_as_billing']		
				shipping.save()
			return redirect('masterfaster:editShippingAddress')
	else:
		u = User.objects.get(username=request.user)
		img = gravatar(u.email)
		try:
			shipping = Shipping.objects.get(user=u)
		except Shipping.DoesNotExist:
			shipping = None
		if shipping != None:
			shipping_address_form = EditShippingAddress(instance=shipping)
		else:
			shipping_address_form = EditShippingAddress()
		context = {
			'address_form': shipping_address_form,
			'edit_profile': False,
			'edit_billing': False,
			'edit_shipping': True,
			'img': img
		}
		return HttpResponse(render(request, 'masterfaster/editprofile.html', context))