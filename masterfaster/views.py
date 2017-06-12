from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse
from masterfaster.models import User, Topic, Article, Billing, Shipping
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms.forms import CreateUserForm, EditEmailAddress
from utils import gravatar, send_email
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
import random

def articles(request, topic_id):
	topic = get_object_or_404(Topic, pk=topic_id)
	context = {}
	context['topic'] = topic
	try:
		articles = Article.objects.filter(topic=topic)
		context['articles_list'] = articles
	except Article.DoesNotExist:
		context['articles_list'] = []
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user)
		img = gravatar(user.email)
		context['img'] = img
	return HttpResponse(render(request, 'masterfaster/articletopic.html', context))

@login_required
def change_password(request):
	user = User.objects.get(username=request.user)
	img = gravatar(user.email)
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			subject = "Master Faster Changed Password"
			message = "You recently changed your password."
			from_email = settings.EMAIL_HOST_USER
			to_email = User.objects.get(username=request.user).email
			send_email(subject, message, from_email, to_email)
			return HttpResponse(render(request, 'masterfaster/editconfirmation.html', {'update': 'Password', 'img':img}))
		else:
			context = {
				'form': PasswordChangeForm(request.user),
				'img': img,
				'errors': form.errors
			}
			return HttpResponse(render(request, 'registration/password_change_form.html', context))
	else:
		form = PasswordChangeForm(request.user)
		context = {
			'form': form,
			'img': img
		}
		return HttpResponse(render(request, 'registration/password_change_form.html', context))

def createUser(request):
	if request.method == 'POST':
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
			form = CreateUserForm(request.POST)
			if form.is_valid():
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
				subject = "Master Faster User Creation"
				message = "Hello %s! Thank you for becoming a member of the MasterFaster community!\n\nBest,\nMaster Faster Team" % user.username
				from_email = settings.EMAIL_HOST_USER
				to_email = user.email
				send_email(subject, message, from_email, to_email)
				billing = Billing(user=user)
				billing.save()
				shipping = Shipping(user=user)
				shipping.save()
				u = authenticate(username=uname, password=password)
				#authenticate new user
				if u is not None:
					login(request, u)
					return redirect('masterfaster:home')
				else:
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

def csrf_failure(request, reason=""):
	context ={}
	if reason:
		context['reason'] = reason
		context['description'] = ''
		context['description'] +=  "Hello from the MasterFaster team! It looks like you have cookies disabled on your device. In order to submit\
		any forms on our site, you must enable cookies to allow us to enforce our Cross Site Request Forgery protection. Thanks! \
		\n If you feel like you've received this message in error, please reach out to us at %s" % settings.EMAIL_HOST_USER
	return HttpResponse(render(request, 'masterfaster/csrf403error.html', context))

def custom_page_not_found(request):
	context = {}
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user)
		img = gravatar(user.email)
		context['img'] = img
	return HttpResponse(render(request, 'masterfaster/404.html', context))

@login_required
def editEmailAddress(request):
	if request.method == 'POST':
		form = EditEmailAddress(request.POST)
		user = User.objects.get(username=request.user)
		if form.is_valid():
			user.email = form.cleaned_data['email']
			user.save()
			return HttpResponse(render(request, 'masterfaster/editconfirmation.html', {'update': 'Email Address'}))
		return redirect('masterfaster:editEmailAddress')
	else:
		u = User.objects.get(username=request.user)
		img = gravatar(u.email)
		form = EditEmailAddress(instance=u)
		context = {
			'form': form,
			'img': img
		}
		return HttpResponse(render(request, 'masterfaster/editemail.html', context))

def home(request):
	context = {}
	if request.user.is_authenticated:
		u = User.objects.get(username=request.user)
		img = gravatar(u.email, 40)
		context['img'] = img
	topics = Topic.objects.all()
	colTypes = ["article-col col-xs-3", 'article-col col-xs-4 col-xs-offset-1', 'article-col col-xs-3 col-xs-offset-1']
	colHeights = ["article-height-small", "article-height-medium", "article-height-tall"]
	topicTups = []
	for i in range(len(topics)):
		r = random.random()
		if r < .33:
			rand = 0
		elif r >= .33 and r < .66:
			rand = 1
		else:
			rand = 2
		c = colTypes[i % len(colTypes)] + " " + colHeights[rand]
		topicTups.append((topics[i], c))
	context['topics'] = topicTups
	return HttpResponse(render(request, 'masterfaster/home.html', context))
