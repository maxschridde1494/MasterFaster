from django.conf.urls import url, include
from . import views
from blog import views as blogviews
from django.contrib.auth import views as auth_views

app_name='masterfaster'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'masterfaster/registration/login.html'}, name='login'),
    url(r'^change_password/$', views.change_password, name='password_change'),
    url(r'^create_user/$', views.createUser, name='createUser'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'masterfaster/registration/logout.html'}, name='logout'),
	url(r'^edit_email/$', views.editEmailAddress, name='editEmailAddress'),
	url(r'^articles/$', views.topics, name='topics'),
	url(r'^articles/(?P<topic_id>[0-9]+)/$', views.articles, name='articles'),
	url(r'^articles/(?P<topic_id>[0-9]+)/(?P<subtopic_id>[0-9]+)/$', views.articles_subtopic, name='articles_subtopic'),
	url(r'^videofeed/$', views.videofeed, name='videofeed'),
]
