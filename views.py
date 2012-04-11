import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

import models


def view(request, slug = ""):
	
	page = get_object_or_404(models.Page, slug = slug)
	page.add_view()
	if request.user.is_authenticated():
		page_user, page_user_created = models.PageUser.objects.get_or_create(user = request.user, page = page, defaults = {"first_view": datetime.datetime.now(), "last_view": datetime.datetime.now(), "views": 0})
		page_user.add_view()
	else:
		page_user = None
	return render_to_response("wiki/view.html", {"page": page, "page_user": page_user}, RequestContext(request))
