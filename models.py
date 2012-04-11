import datetime

from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
	slug = models.SlugField(max_length = 30, blank = True, db_index = True, unique = True, primary_key = True)
	title = models.CharField(max_length = 100)
	first_revision = models.ForeignKey("PageRevision", related_name = "+", null = True, blank = True)
	current_revision = models.ForeignKey("PageRevision", related_name = "+", null = True, blank = True)
	views = models.IntegerField(blank = True)
	next_revision_num = models.IntegerField(blank = True)
	
	def add_view(self):
		self.views += 1
		self.save()
		
	def get_absolute_url(self):
		return "/wiki/view/" + self.slug + "/"
		
	def __unicode__(self):
		return self.title
		
class PageRevision(models.Model):
	page = models.ForeignKey("Page", db_index = True)
	num = models.IntegerField(blank = True)
	author = models.ForeignKey(User, blank = True)
	create_date = models.DateTimeField(blank = True)
	previous_revision = models.ForeignKey("PageRevision", null = True, blank = True)
	content = models.TextField(max_length = 100000, blank = True)
	reverted = models.BooleanField(blank = True)
	revert_reason = models.TextField(max_length = 50, blank = True)
	
	def get_absolute_url(self):
		return "/wiki/view/" + self.page.slug + "/revision/" + str(self.num) + "/"
		
	def __unicode__(self):
		return self.page.title + " (" + str(self.create_date) + ")"
		
class PageUser(models.Model):
	user = models.ForeignKey(User, related_name = "page_set", db_index = True)
	page = models.ForeignKey(Page, related_name = "user_set", db_index = True)
	first_view = models.DateTimeField(blank = True)
	last_view = models.DateTimeField(blank = True)
	views = models.IntegerField(blank = True)
	
	def add_view(self):
		self.views += 1
		self.last_view = datetime.datetime.now()
		self.save()
		
	def __unicode__(self):
		return self.user.userprofile.display_name + " on " + self.page.title
		
