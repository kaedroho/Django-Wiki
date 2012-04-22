from django import forms
from django.conf import settings

import models


class CreateForm(forms.Form):
	title = forms.CharField()
	content = forms.CharField(widget = forms.widgets.Textarea(attrs = {"rows": 15, "cols": 80}))
	
class EditForm(forms.Form):
	content = forms.CharField(widget = forms.widgets.Textarea(attrs = {"rows": 15, "cols": 80}))
