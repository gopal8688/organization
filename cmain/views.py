from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from auths.models import Customer, Property, CPRelationship, PropertyTokens
from base.views import BaseView
from django.http import HttpResponse

class CMain(BaseView):

	def __init__(self):
		BaseView.__init__(self)

	def getAbsoluteURL(self, request):
		full_url = request.get_host()
		is_https = request.is_secure()

		if is_https:
			full_url = "https://%s/"%full_url
		else:
			full_url = "http://%s/"%full_url

		return full_url

	def valiDateProperty(self, request, id):
		cust_obj = self.getCustomerObj(request)
		prop_obj = Property.objects.filter(properties__email=cust_obj.email, id=id)
		if not prop_obj:
			return False
		else:
			return True


	def getBasicDetails(self, request, id):

		cust_obj = self.getCustomerObj(request)

		cust_full_name = "%s %s"%(cust_obj.fname, cust_obj.lname)
		#print ('JSONss', self.SITE_DATA['API_URLS'])

		context = {
			'cust_email': cust_obj.email,
			'cust_full_name': cust_full_name,
			'request': request,
			'base_url': self.getAbsoluteURL(request),
			'API_KEY': 'eiWee8ep9due4deeshoa8Peichai8Eih',
		}

		request.session['pid'] = id
		prop_obj = self.getPropertyObj(request)

		properties = Property.objects.filter(properties__email=cust_obj.email)

		if properties:
			context.update({
				'rows': properties,
				'show_row': prop_obj,
				'company': prop_obj.pname,
				'pid': request.session['pid'],
			})
		# if not prop_obj:
		# 	request.session['pid'] = 0
		# else:
		# 	request.session['pid'] = prop_obj[0].id
		# 	context.update({
		# 		'rows': prop_obj,
		# 		'show_row': prop_obj[0],
		# 		'company': prop_obj[0].pname,
		# 		'pid': request.session['pid'],
		# 	})

		# print(request.session['pid'])
		# return str(request.session['pid'])
		# Saving into session.
		self.SITE_DATA.update(context)
	def setFirstProperty(self, request):
		cust_obj = self.getCustomerObj(request)
		prop_obj = Property.objects.filter(properties__email=cust_obj.email)

		if not prop_obj:
			request.session['pid'] = 0
		else:
			request.session['pid'] = prop_obj[0].id
		#return request.session['pid']

#property_create_view = PropertyView.as_view();