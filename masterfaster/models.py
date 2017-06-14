from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone
import datetime

class User(AbstractUser):
	username=models.CharField(primary_key=True, unique=True, max_length=50)
	email = models.EmailField(max_length=200)
	password = models.CharField(max_length=200)

	def __str__(self):
		return self.username

class Topic(models.Model):
	topic = models.CharField(unique=True, max_length=50)

	def __str__(self):
		return self.topic

class SubTopic(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	subtopic = models.CharField(max_length=100)

	def __str__(self):
		return self.subtopic

class Article(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	subtopic = models.ForeignKey(SubTopic, null=True)
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	description = models.CharField(max_length=300)
	link = models.CharField(max_length=300)

	def __str__(self):
		return self.title

class Address(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=50, null=True)
	city = models.CharField(max_length=20, null=True)
	state = models.CharField(max_length=50, null=True)
	zipcode = models.IntegerField(default=00000, null=True)
	country = models.CharField(max_length=50, null=True)

	class Meta:
	    abstract = True

class Billing(Address):
	def __str__(self):
		return self.user.username

class Shipping(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=20, null=True, blank=True)
	state = models.CharField(max_length=50, null=True, blank=True)
	zipcode = models.IntegerField(default=00000, null=True, blank=True)
	country = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		return self.user.username
