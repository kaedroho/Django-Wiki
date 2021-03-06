import datetime
import difflib

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required

import models
import forms


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
		
	page.add_view()
	
	last_view_revision = 0
	if request.user.is_authenticated():
		page_user, page_user_created = models.PageUser.objects.get_or_create(user = request.user, page = page, defaults = {"last_view_revision": revision.num})
		last_view_revision = page_user.last_view_revision
		page_user.add_view()
	else:
		page_user_created = False
		page_user = None
		
	page_changed = False
	if request.user.is_authenticated() and last_view_revision != page.current_revision.num and not page_user_created:
		page_changed = True
	return render_to_response("wiki/view.html", {"page": page, "revision": revision, "page_user": page_user, "page_changed": page_changed, "first_view": page_user_created}, RequestContext(request))
	
@login_required
def create(request):
	if request.method == "POST":
		form = forms.CreateForm(request.POST)
		if form.is_valid():
			new_page = models.Page()
			new_page.title = form.cleaned_data["title"]
			new_page.slug = slugify(new_page.title)
			try:
				models.Page.objects.get(slug = new_page.slug)
			except:
				new_page.save()
				new_page.add_revision(request.user, request.META["REMOTE_ADDR"], form.cleaned_data["content"])
				return redirect(new_page.get_absolute_url())
	else:
		form = forms.CreateForm()
		
	return render_to_response("wiki/create.html", {"form": form}, RequestContext(request))
	
@login_required
def edit(request, slug = ""):
	page = get_object_or_404(models.Page, slug = slug)
	
	if request.method == "POST":
		form = forms.EditForm(request.POST)
		if form.is_valid():
			page.add_revision(request.user, request.META["REMOTE_ADDR"], form.cleaned_data["content"])
			return redirect(page.get_absolute_url())
	else:
		form = forms.EditForm({"content": page.current_revision.content})
		
	return render_to_response("wiki/edit.html", {"page": page, "form": form}, RequestContext(request))
	
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
	
def diff(request, slug = "", rev_from_str = "0", rev_to_str = "0"):
	page = get_object_or_404(models.Page, slug = slug)
	
	#Check get parameter
	if "since" in request.GET:
		rev_from_str = request.GET["since"]
		
	#Get revision to
	try:
		rev_to_num = int(rev_to_str)
	except ValueError:
		raise Http404
	if rev_to_num == 0:
		revision_to = page.current_revision
	else:
		revision_to = get_object_or_404(models.PageRevision, page = page, num = rev_to_num)
		
	#Get revision from
	try:
		rev_from_num = int(rev_from_str)
	except ValueError:
		raise Http404
	if rev_from_num == 0:
		if revision_to.previous_revision:
			revision_from = revision_to.previous_revision
		else:
			revision_from = page.current_revision
	else:
		revision_from = get_object_or_404(models.PageRevision, page = page, num = rev_from_num)
		
	#Check if the from number is higher than the to number
	if revision_from.num > revision_to.num:
		raise Http404
		
	from_lines = revision_from.content.splitlines(True)
	to_lines = revision_to.content.splitlines(True)
	
	d = difflib.Differ()
	diff = d.compare(from_lines, to_lines)
	
	diff_html = ""
	for line in diff:
		diff_html = diff_html + line + "\n"
		
	return render_to_response("wiki/diff.html", {"page": page, "revision_from": revision_from, "revision_to": revision_to, "diff": diff_html}, RequestContext(request))
	
