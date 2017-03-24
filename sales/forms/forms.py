from datetime import date, datetime
from calendar import monthrange
from django.forms import ModelForm
from masterfaster.models import CreditCard
from django import forms
from sales.models import Sale

class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ["number", 'exp_date_month', 'exp_date_year', 'csv']
    
    def clean(self):
        cleaned = super(CreditCardForm, self).clean()
        if not self.errors:
            #check for number errors
            if self.cleaned_data['number'] and (len(self.cleaned_data['number']) < 13 or len(self.cleaned_data['number']) > 16):
                raise forms.ValidationError("Please enter in a valid credit card number.")
            #check for expiration date errors
            months = [str(x) for x in range(1,13)] + ['0'+str(x) for x in range(1,13)]
            if self.cleaned_data['exp_date_month'] not in months:
                raise forms.ValidationError("Not a valid month.")
            if date.today().year > int(self.cleaned_data['exp_date_year']):
                raise forms.ValidationError("The expiration date you entered is in the past.")
            if int(self.cleaned_data['exp_date_year']) >= date.today().year and int(self.cleaned_data['exp_date_month']) < date.today().month:
                raise forms.ValidationError("The expiration date you entered is in the past.")
        return cleaned
