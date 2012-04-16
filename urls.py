from django.conf.urls.defaults import *

import views


urlpatterns = patterns("",
#	url(r"^random/$", views.random),
#	url(r"^create/$", views.create),
	url(r"^(?P<slug>[^/]*)/$", views.view),
	url(r"^(?P<slug>[^/]*)/revision/(?P<revision_str>[^/]*)/$", views.view),
	url(r"^(?P<slug>[^/]*)/history/$", views.history),
#	url(r"^(?P<slug>[^/]*)/edit/$", views.edit),
)
