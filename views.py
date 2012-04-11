import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404

import models


def view(request, slug = "", revision_str = "0"):
	page = get_object_or_404(models.Page, slug = slug)
	
	try:
		revision_num = int(revision_str)
	except ValueError:
		raise Http404
		
	if revision_num == 0:
		revision = page.current_revision
	else:
		revision = get_object_or_404(models.PageRevision, page = page, num = revision_num)
		
	page = get_object_or_404(models.Page, slug = slug)
	page.add_view()
	
	if request.user.is_authenticated():
		page_user, page_user_created = models.PageUser.objects.get_or_create(user = request.user, page = page, defaults = {"first_view": datetime.datetime.now(), "last_view": datetime.datetime.now(), "views": 0})
		page_user.add_view()
	else:
		page_user = None
		
	return render_to_response("wiki/view.html", {"page": page, "revision": revision, "page_user": page_user}, RequestContext(request))
	
def history(request, slug = ""):
	page = get_object_or_404(models.Page, slug = slug)
	revision_list = page.pagerevision_set.all().order_by("-num")
	
	paginator = Paginator(revision_list, 25)
	try:
		page_num = int(request.GET.get("page", "1"))
	except ValueError:
		page_num = 1
		
	try:
		revisions = paginator.page(page_num)
	except (EmptyPage, InvalidPage):
		revisions = paginator.page(paginator.num_pages)
		
	return render_to_response("wiki/history.html", {"page": page, "revisions": revisions}, RequestContext(request))
	
