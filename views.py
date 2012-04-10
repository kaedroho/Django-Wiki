from django.shortcuts import render_to_response
from django.template import RequestContext


def view(request, slug = ""):
	return render_to_response("wiki/view.html", {}, RequestContext(request))