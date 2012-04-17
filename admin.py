from django.contrib import admin
from django.template.defaultfilters import slugify

import models


class PageAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if not obj.slug:
			obj.slug = slugify(obj.title)
			obj.next_revision_num = 2
			obj.save()
			
			first_revision = models.PageRevision()
			first_revision.page = obj
			first_revision.num = 1
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
			obj.num = obj.page.next_revision_num
			obj.author = request.user
			obj.previous_revision = obj.page.current_revision
			obj.save()
			
			obj.page.current_revision = obj
			obj.page.next_revision_num = obj.page.next_revision_num + 1
			obj.page.save()
		else:
			obj.save()
			
admin.site.register(models.Page, PageAdmin)
admin.site.register(models.PageRevision, PageRevisionAdmin)
admin.site.register(models.PageUser)
