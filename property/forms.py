from django import forms
import re

class DNTrackIPForm(forms.Form):
	dnt_ip = forms.RegexField(regex=re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'))
    
class DNTrackIPrangeForm(forms.Form):
	dnt_ip = forms.RegexField(regex=re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/([0-9]|[1-2][0-9]|3[0-2])$'))

class DNTrackEmailForm(forms.Form):
	email = forms.RegexField(regex=re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'))

class DNTrackDomainForm(forms.Form):
	email = forms.RegexField(regex=re.compile(r'\A([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\Z'))

class WebhookForm(forms.Form):
	url = forms.RegexField(regex=re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'))
	options = forms.CharField(max_length=150)
	is_active = forms.BooleanField()

class CustomizeAlertsForm(forms.Form):
	app_uid = forms.RegexField(regex=re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'))
	risk_threshold = forms.CharField(max_length=150)
	is_active = forms.BooleanField()

