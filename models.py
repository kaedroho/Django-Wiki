from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
	slug = models.SlugField(max_length = 30, blank = True, db_index = True, unique = True, primary_key = True)
	title = models.CharField(max_length = 100)
	first_revision = models.ForeignKey("PageRevision", related_name = "+", null = True, blank = True)
	current_revision = models.ForeignKey("PageRevision", related_name = "+", null = True, blank = True)
	views = models.IntegerField(blank = True)
	
	def get_absolute_url(self):
		return "/wiki/view/" + self.slug + "/"
		
	def __unicode__(self):
		return self.title
		
class PageRevision(models.Model):
	page = models.ForeignKey("Page", db_index = True)
	author = models.ForeignKey(User, blank = True)
	create_date = models.DateTimeField(blank = True)
	previous_revision = models.ForeignKey("PageRevision", null = True, blank = True)
	content_wiki = models.TextField(max_length = 100000, blank = True)
	content_html = models.TextField(max_length = 100000, blank = True)
	
	def __unicode__(self):
		return self.page.title + " (" + str(self.create_date) + ")"
		
