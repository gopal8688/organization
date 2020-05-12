# from django import forms
# import re

# class DNTrackIPForm(forms.Form):
# 	# brand_name = forms.CharField(max_length=150,required=False)
# 	# brand_url = forms.URLField(required=False)
# 	# brand_logo = forms.ImageField(required=False)
# 	# org_name = forms.CharField(max_length=150)
# 	dnt_ip = forms.CharField(max_length=150)
# 	ipRegex = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
# 	ipRangeRegex = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/([0-9]|[1-2][0-9]|3[0-2])$'
# 	if((re.search(ipRegex, dnt_ip))):
# 		dnt_ip = 
# 	elif((re.search(ipRangeRegex, dnt_ip))):
# 		dnt_ip
# 	else:
# 		data = {
# 				'status': 'error',
# 				'message': 'Please enter valid IP address or IP range'
# 				}

