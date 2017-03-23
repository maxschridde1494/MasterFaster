from django.db import models

from django.conf import settings
from django.utils import timezone
import datetime

class Sale(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#import stripe and set the api_key
		import stripe
		stripe.api_key = settings.STRIPE_API_KEY
		self.stripe = stripe
	#have sale store the stripe charge id
	charge_id = models.CharField(max_length=32)
	#STORE OTHER INFO

	def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
		"""Input: price and the credit card details.
		Output: tuple (Boolean, Class)
			- True if charge is successful
			- Class --> response or error instance
		"""
		#don't charge the card if already charged
		if self.charge_id:
			return (False, Exception(message="This card has already been charged."))
		try:
			response = self.stripe.Charge.create(
				amount = price_in_cents,
				currency = 'usd',
				source = {
					'number': number,
					'exp_month': exp_month,
					'exp_year': exp_year,
					'cvc': cvc,
					'object': "card",
					####Include billing address somehow
				},
				description = 'Thanks for the purchase!')
			self.charge_id = response.id
		except self.stripe.error.CardError as ce:
			#charge of card failed
			# Since it's a decline, stripe.error.CardError will be caught
			body = ce.json_body
			err  = body['error']
			print ("Status is: %s" % ce.http_status)
			print ("Type is: %s" % err['type'])
			print ("Code is: %s" % err['code'])
			print ("Param is: %s" % err['param'])
			print ("Message is: %s" % err['message'])
			return (False, ce)
		except self.stripe.error.AuthenticationError as e:
			# Authentication with Stripe's API failed
			print('Authentication Error')
			return (False, e)
		return (True, response)