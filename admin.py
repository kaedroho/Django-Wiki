import datetime

from django.contrib import admin
from django.template.defaultfilters import slugify

import models


class PageAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if not obj.slug:
			obj.slug = slugify(obj.title)
			obj.views = 0
			obj.save()
			
			first_revision = models.PageRevision()
			first_revision.page = obj
			first_revision.author = request.user
			first_revision.create_date = datetime.datetime.now()
			first_revision.save()
			
			obj.first_revision = first_revision
			obj.current_revision = first_revision
			obj.save()
		else:
			obj.save()
			
class PageRevisionAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if not obj.id:
			obj.author = request.user
			obj.create_date = datetime.datetime.now()
			obj.previous_revision = obj.page.current_revision
			obj.save()
			obj.page.current_revision = obj
			obj.page.save()
		else:
			obj.save()
			
admin.site.register(models.Page, PageAdmin)
admin.site.register(models.PageRevision, PageRevisionAdmin)
