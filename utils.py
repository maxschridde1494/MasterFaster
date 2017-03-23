import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
 
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
    return mark_safe('<img class=%s src="%s" height="%d" width="%d">' % (classes, url, size, size))


def fetch_prev_next(bp, posts):
	"""Takes in a blog post and the QuerySet of all blog posts.
	Returns a dictionary mapping:
	{'first': boolean,
	'last': boolean,
	'prev': blog_post,
	'next': blog_post}

	"""
	found, counter = False, 0
	while not found and counter < len(posts):
		if posts[counter] == bp:
			found = True
		else:
			counter += 1
	p_n = {'prev': None,'next': None}
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