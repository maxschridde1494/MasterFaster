from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

from django.conf import settings
from django.utils import timezone
import datetime
from masterfaster.models import User

class Product(models.Model):
	def size_default():
		return {"small": "S", 'medium': 'M', 'large': 'L', 'x-large': 'XL'}

	name = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.CharField(max_length=400, null=True)
	img_path = models.CharField(max_length=200, default='sales/images/default.jpg')
	size = JSONField("Size", default=size_default)

	def __str__(self):
		return self.name

class ShoppingCart(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	#store product ids in shopping Cart model
	items = ArrayField(models.IntegerField(), default=[])

	def __str__(self):
		return self.user.username


class Sale(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		import stripe
		stripe.api_key = settings.STRIPE_API_KEY_SECRET
		self.stripe = stripe
	#have sale store the stripe charge id
	charge_id = models.CharField(max_length=32, null=True)
	date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
	amount = models.CharField(max_length=100, null=True)
	user = models.ForeignKey(User, null=True)

	def __str__(self):
		return self.charge_id

	# def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
	def charge(self, price_in_cents, token):
		"""Input: price and the stripeToken from CHECKOUT.
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
				source = token,
				description = 'Thanks for the purchase!')
			self.charge_id = response.id
		except self.stripe.error.CardError as ce:
			#charge of card failed
			body = ce.json_body
			err  = body['error']
			print ("Status is: %s" % ce.http_status)
			print ("Type is: %s" % err['type'])
			print ("Code is: %s" % err['code'])
			print ("Message is: %s" % err['message'])
			return (False, ce)
		except self.stripe.error.AuthenticationError as e:
			# Authentication with Stripe's API failed
			print('Authentication Error')
			return (False, e)
		return (True, response)