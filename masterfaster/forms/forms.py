from django import forms
from django.forms import ModelForm
from masterfaster.models import User, Billing, Shipping
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(forms.ModelForm):
	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput,)
        # help_text="Enter the same password as above, for verification.")
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		widgets = {'password': forms.PasswordInput}

class EditUserInfo(ModelForm):
	class Meta:
		model = User
		fields = ['email', 'credit_card_number', 'credit_card_exp_date_month', 'credit_card_exp_date_year', 'credit_card_csv']

class EditBillingAddress(ModelForm):
	class Meta:
		model = Billing
		fields = ['address', 'city', 'state', 'zipcode', 'country']

class EditShippingAddress(ModelForm):
	class Meta:
		model = Shipping
		fields = ['address', 'city', 'state', 'zipcode', 'country', 'same_as_billing']