from django.contrib import admin
from django.template.defaultfilters import slugify

import models


class PageAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if not obj.slug:
			obj.slug = slugify(obj.title)
			obj.save()
			
			obj.add_revision(request.user, request.META["REMOTE_ADDR"], "Test Content")
		else:
			obj.save()
			
class PageRevisionAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if not obj.id:
			obj.num = obj.page.next_revision_num
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
