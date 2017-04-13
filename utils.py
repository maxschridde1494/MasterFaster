import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
from sales.models import Product, ShoppingCartItems
from datetime import datetime
import functools
from django.core.mail import send_mail, BadHeaderError
 
register = template.Library()
 
# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=40):
  default = "mm"
  #strip whitespace of email
  email = email.strip()
  return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower().encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d':default, 's':str(size)}))
 
# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=40, classes="img-circle center-block base-profile"):
    url = gravatar_url(email, size)
    return mark_safe('<img class="%s" src="%s" height="%d" width="%d">' % (classes, url, size, size))

def dollar_str_to_cents_int(num):
	s = str(num).split('.')
	doll = int(s[0])
	if len(s) > 1:
		return doll*100 + int(s[1])
	return doll*100

def address_empty(address):
	if address.address == None or address.city == None or address.state == None or address.zipcode == None or address.country == None:
		return True
	return False

def cents_to_dollars(num):
	"""return string in $0.00 format"""
	if int(num) < 100:
		return "$0." + num
	dollars,cents = str(int(num) // 100), str(int(num) % 100)
	if len(cents) < 2:
		cents = "0" + cents
	return "$" + dollars + "." + cents

def create_blog_months():
	"""Generate months for sidebarcontent of blog feed
	return [(month_string, year_string, int representing month)]
	"""
	months = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September','10':'Octoboer','11':'November','12':'December'}
	today = datetime.today()
	month, year = today.month, today.year
	month_year_arr = []
	for i in range(1,13):
		m_str = months[str(((i + month)%12))] if (i+month)%12 != 0 else months['12']
		y_str = str(year - 1) if i + month <= 12 else str(year)
		month_year_arr.insert(0,(m_str, y_str, str((i + month)%12)))
	return month_year_arr

def fetch_prev_next(bp, posts):
	"""Takes in a blog post and the QuerySet of all blog posts.
	Returns a dictionary mapping:
	{'first': boolean,
	'last': boolean,
	'prev': blog_post,
	'next': blog_post}

	"""
	found, counter = False, 0
	p_n = {'prev': None,'next': None, 'first': False, 'last': False}
	if len(posts) == 0:
		return p_n
	while not found and counter < len(posts):
		if posts[counter] == bp:
			found = True
		else:
			counter += 1
	if counter == 0:
		p_n['first'] = True
		if counter < len(posts) - 1:
			p_n['last'] = False
			p_n['next'] = posts[counter + 1].id
	if counter == len(posts) - 1:
		p_n['last'] = True
		if counter > 0:
			p_n['first'] = False
			p_n['prev'] = posts[counter - 1].id
	if counter > 0 and counter < len(posts) - 1:
		p_n['first'] = False
		p_n['last'] = False
		p_n['prev'] = posts[counter - 1].id
		p_n['next'] = posts[counter + 1].id
	return p_n

def get_shopping_cart_total_price(user):
	products = ShoppingCartItems.objects.filter(user=user) 
	items = [(Product.objects.get(pk=p.pid),p) for p in products]
	if items:
		prices = [item[1].quantity*item[0].price for item in items]
		total_price = functools.reduce(lambda x,y: x+y, prices, 0)
	else:
		total_price = 0.00
	return total_price

def send_email(subject, message, from_email, to_email):
	if subject and message and from_email:
		try:
			send_mail(subject, message, from_email, [to_email])
		except BadHeaderError:
			print('Email could not be sent.')

