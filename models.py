import datetime

from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
	slug = models.SlugField(max_length = 30, blank = True, db_index = True, unique = True, primary_key = True)
	title = models.CharField(max_length = 100)
	current_revision = models.ForeignKey("PageRevision", related_name = "+", null = True, blank = True)
	views = models.IntegerField(blank = True, default = 0)
	next_revision_num = models.IntegerField(blank = True, default = 1)
	
	def add_view(self):
		self.views += 1
		self.save()
		
	def add_revision(self, user, content):
		new_revision = PageRevision()
		new_revision.page = self
		new_revision.num = self.next_revision_num
		new_revision.author = user
		new_revision.previous_revision = self.current_revision
		new_revision.content = content
		new_revision.save()
		
		self.current_revision = new_revision
		self.next_revision_num = self.next_revision_num + 1
		self.save()
		
	def get_absolute_url(self):
		return "/wiki/" + self.slug + "/"
		
	def __unicode__(self):
		return self.title
		
class PageRevision(models.Model):
	page = models.ForeignKey("Page", db_index = True)
	num = models.IntegerField(blank = True)
	author = models.ForeignKey(User, related_name = "pagerevision_set_created")
	create_date = models.DateTimeField(blank = True, default = datetime.datetime.now)
	previous_revision = models.ForeignKey("PageRevision", null = True, blank = True)
	content = models.TextField(max_length = 100000, blank = True)
	reverted = models.BooleanField(blank = True)
	revert_reason = models.TextField(max_length = 50, blank = True)
	revert_user = models.ForeignKey(User, null = True, blank = True, related_name = "pagerevision_set_reverted")
	
	def get_absolute_url(self):
		return "/wiki/" + self.page.slug + "/revision/" + str(self.num) + "/"
		
	def __unicode__(self):
		return self.page.title + " (Revision " + str(self.num) + ")"
		
class PageUser(models.Model):
	user = models.ForeignKey(User, related_name = "page_set", db_index = True)
	page = models.ForeignKey(Page, related_name = "user_set", db_index = True)
	first_view = models.DateTimeField(blank = True, default = datetime.datetime.now)
	last_view = models.DateTimeField(blank = True, default = datetime.datetime.now)
	last_view_revision = models.IntegerField(blank = True, default = 1)
	views = models.IntegerField(blank = True, default = 0)
	
	def add_view(self):
		self.views += 1
		self.last_view = datetime.datetime.now()
		if self.last_view_revision < self.page.current_revision.num:
			self.last_view_revision = self.page.current_revision.num
		self.save()
		
	def __unicode__(self):
		return self.user.userprofile.display_name + " on " + self.page.title
		
