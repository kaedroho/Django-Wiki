from django.conf.urls.defaults import *

import views


urlpatterns = patterns("",
	url(r"^view/(?P<slug>[^/]*)/$", views.view),
	url(r"^view/(?P<slug>[^/]*)/revision/(?P<revision_str>[^/]*)/$", views.view),
	url(r"^history/(?P<slug>[^/]*)/$", views.history),
#	url(r"^edit/(?P<slug>\d{8})/", views.edit),
#	url(r"^view/random/", views.random),
#	url(r"^create/", views.create),
)
