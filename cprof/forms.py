from django import forms

class CompanyForm(forms.Form):
	brand_name = forms.CharField(max_length=150,required=False)
	brand_url = forms.URLField(required=False)
	brand_logo = forms.ImageField(required=False)
	org_name = forms.CharField(max_length=150)