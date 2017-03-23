from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime

class BlogPost(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	header_text = models.TextField(null=True)
	text = models.TextField()

	def __str__(self):
		return self.title

class Comment(models.Model):
	blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	text = models.TextField()
	pub_date = models.DateTimeField('date published')
