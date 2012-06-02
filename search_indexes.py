from haystack import indexes, site

import models


class PageIndex(indexes.SearchIndex):
	text = indexes.CharField(document = True, use_template = True)
	
	def get_model(self):
		return models.Page
		
	def index_queryset(self):
		return self.get_model().objects.all()
		
site.register(models.Page, PageIndex)
