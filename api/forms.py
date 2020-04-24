from django import forms

class HighRiskUsersForm(forms.Form):
	dur = forms.CharField(max_length=150)
	limit = forms.IntegerField()
class DashboardStatsForm(forms.Form):
	dur = forms.CharField(max_length=150)
class SecurityAlertsForm(forms.Form):
	dur = forms.CharField(max_length=150)
	limit = forms.IntegerField()
class LoginAttemptsForm(forms.Form):
	dur = forms.CharField(max_length=150)
class UserRiskAnalyticsForm(forms.Form):
	dur = forms.CharField(max_length=150)
class RegionRiskForm(forms.Form):
	dur = forms.CharField(max_length=150)
class RiskMapForm(forms.Form):
	dur = forms.CharField(max_length=150)
class UsersListForm(forms.Form):
	dur = forms.CharField(max_length=150)
	limit = forms.IntegerField()
class BasicUserDetailsForm(forms.Form):
	user = forms.CharField(max_length=150)
class UserDetailsLimitForm(forms.Form):
	user = forms.CharField(max_length=150)
	limit = forms.IntegerField()
		