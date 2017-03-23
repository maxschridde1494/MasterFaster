from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404
from .models import BlogPost, Comment
from masterfaster.models import User
from django.conf import settings
from django.utils import timezone
import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from utils import gravatar, fetch_prev_next

month_year = [("March", "2017", "3"),("February", "2017", "2"),("January", "2017", "1"),("December", "2016", "12"),("November", "2016", "11"),("October", "2016", "10"),("September", "2016", "9"),("August", "2016", "8"),("July", "2016", "7"), ("June", "2016", "6"),("May", "2016", "5"),("April", "2016", "4")]

def blogfeed(request):
	blog_posts = BlogPost.objects.order_by('-pub_date')
	auth_post = [(post, User.objects.get(username=post.author), gravatar(User.objects.get(username=post.author).email, 100)) for post in blog_posts]
	context = {
        'blog_posts_list': auth_post,
        'month_year': month_year
    } 
    #if logged in, add user img to navbar
	try:
		u = User.objects.get(username=request.user)
	except User.DoesNotExist:
		return HttpResponse(render(request, 'blog/blogfeed.html', context))
	img = gravatar(u.email, 40)
	context['img'] = img
	return HttpResponse(render(request, 'blog/blogfeed.html', context))

def blogfeed_month(request, year, month):
	posts = get_list_or_404(BlogPost.objects.order_by('-pub_date'), pub_date__month=month, pub_date__year=year)
	filtered = [(post, User.objects.get(username=post.author), gravatar(User.objects.get(username=post.author).email, 100)) for post in posts]
	context = {
		'blog_posts_list': filtered,
		'month_year': month_year
	}
	return HttpResponse(render(request, 'blog/blogfeed.html', context))

def detail(request, entry_id):
	bp = get_object_or_404(BlogPost, pk=entry_id)
	#retrieve previous and next posts
	posts = get_list_or_404(BlogPost.objects.order_by('-pub_date'))
	p_n = fetch_prev_next(bp, posts)
	
	context = {'entry': bp,
		'prev_next': p_n
	}
	context['author_img'] = gravatar(User.objects.get(username=bp.author).email, 100)
	c = bp.comment_set.order_by('-pub_date')
	comments = [(comment, comment.user.username, gravatar(comment.user.email, 50, "img-circle comment-pic")) for comment in c]
	context['comments'] = comments
	if request.user.is_authenticated:
		template="blog/blogdetailloggedin.html"
		context['img'] = gravatar(User.objects.get(username=request.user).email)
	else:
		template = 'blog/blogdetail.html'
	return HttpResponse(render(request, template, context))

def comment(request, entry_id):
	print("in comment")
	bp = get_object_or_404(BlogPost, pk=entry_id)
	c = Comment(user=request.user,blogpost=bp,text=request.POST['comment-text'], pub_date=timezone.now())
	c.save()
	return redirect('blog:detail', entry_id=entry_id)

def newEntry(request):
	context = {'max_date': timezone.now().date()}
	return HttpResponse(render(request, 'masterfaster/blogentry.html', context))