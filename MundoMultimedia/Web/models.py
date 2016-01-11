from django.db import models
from datetime import datetime, time, date
import time
from django.contrib import admin
from PIL import Image
# Create your models here.

class User(models.Model):
	nick = models.CharField(max_length=100, blank = False, unique=True)
	email = models.CharField(max_length=100, blank = False, unique=True)
	password = models.CharField(max_length=100, blank = False)
	name = models.CharField(max_length=100, blank = True)
	surname = models.CharField(max_length=100, blank = True)
	age = models.IntegerField(blank = True, null=True, default=0)
	gender = models.CharField(max_length=100, blank = True)
	vip = models.BooleanField(default = False, blank = False)
	imagen = models.ImageField(upload_to='Web/static/photos/users/', default='Web/static/photos/users/default.png', blank=True)
	def __unicode__(self):
		return self.nick


class Section(models.Model):
	name = models.CharField(max_length=100, blank = False, unique=True)
	def __unicode__(self):
		return self.name

class New(models.Model):
	title = models.CharField(max_length=100, blank = False)
	description = models.TextField(max_length=10000, blank = False)
	date = models.DateField(blank=False, default=datetime.now)
	time = models.IntegerField(blank=True, default=time.time())
	author = models.ForeignKey(User, blank=False)
	section = models.ManyToManyField(Section, blank=True)
	punctuation = models.IntegerField(default=0)
	votes = models.IntegerField(default=0)
	image = models.ImageField(upload_to='Web/static/photos/news', blank=True)
	def __unicode__(self):
		return self.title

class Comment(models.Model):
	description = models.TextField(max_length=10000, blank = False)
	author = models.ForeignKey(User, blank=False)
	date = models.DateField(blank=False, default=datetime.now)
	time = models.IntegerField(blank=True, default=time.time())
	new = models.ForeignKey(New, blank= False)
	def __unicode__(self):
		return self.description

class Vote(models.Model):
	calification = models.IntegerField(blank=False, default=5 )
	author = models.ForeignKey(User, blank=False)
	new = models.ForeignKey(New, blank=False)
		
admin.site.register(User)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(New)
admin.site.register(Vote)
