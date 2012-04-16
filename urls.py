from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

import views


urlpatterns = patterns("",
	url(r"^$", redirect_to, {"url": "/wiki/wiki/"}),
#	url(r"^random/$", views.random),
#	url(r"^create/$", views.create),
	url(r"^(?P<slug>[^/]*)/$", views.view),
	url(r"^(?P<slug>[^/]*)/revision/(?P<revision_str>[^/]*)/$", views.view),
	url(r"^(?P<slug>[^/]*)/history/$", views.history),
#	url(r"^(?P<slug>[^/]*)/edit/$", views.edit),
)
