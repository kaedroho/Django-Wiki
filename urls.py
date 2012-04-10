from django.conf.urls.defaults import *

import views


urlpatterns = patterns("",
	url(r"^view/(?P<slug>\d{8})/", views.view),
#	url(r"^edit/(?P<slug>\d{8})/", views.edit),
#	url(r"^view/random/", views.random),
#	url(r"^create/", views.create),
)