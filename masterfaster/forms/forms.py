from django import forms
from django.forms import ModelForm
from masterfaster.models import User, Billing, Shipping, CreditCard
from sales.forms.forms import CreditCardForm
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(ModelForm):
	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput,)
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		widgets = {'password': forms.PasswordInput}

class EditEmailAddress(ModelForm):
	class Meta:
		model = User
		fields = ['email']

class EditBillingAddress(ModelForm):
	class Meta:
		model = Billing
		fields = ['address', 'city', 'state', 'zipcode', 'country']

class EditShippingAddress(ModelForm):
	class Meta:
		model = Shipping
		fields = ['address', 'city', 'state', 'zipcode', 'country']