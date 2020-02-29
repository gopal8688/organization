from django.shortcuts import render
from django.utils.crypto import get_random_string

from django.views import View
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from cmain.views import CMain
from auths.models import Customer,Property,CPRelationship,WebPlatform,PropertyTokens
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime

import os

# Create your views here.
class PropertyCreateView(View, CMain):
	"""docstring for PropertyCreateView"""
	def __init__(self, **arg):
		super(PropertyCreateView, self).__init__()
		self.arg = arg
	
	def get(self, request):
		self.SITE_DATA['page'] = 'property_create'
		self.SITE_DATA['page_title'] = 'Create Property'
		self.SITE_DATA['form_url'] = reverse('propertyCreate')
		return render(request, 'property_create.html', self.SITE_DATA)

	def post(self, request):
		try:
			pn = request.POST['pn']
			p = Property(pid=get_random_string(length=16, allowed_chars='123456789'), pname = pn, country="India")
			p.save()

			if p.id:
				c_obj = Customer.objects.get(email=request.session['email'])
				cp = CPRelationship(cust=c_obj,prop=p,role='S')
				cp.save()
				data = {
					'status': 'success',
					'red_url': reverse('psplatforms', args=[p.id]),
				}
			else:
				data = {
					'status': 'error',
					'message': 'There was some error.',
				}
			return JsonResponse(data)
		except:
			return JsonResponse({
					'status': 'error',
					'message': 'There was some error. Please refresh and try again.',
				})
class PropertySettingsView(View, CMain):
	""" docstring for PropertySettingsView """
	def __init__(self, **arg):
		super(PropertySettingsView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		if(not self.valiDateProperty(request, id)):
			redirect('home')
		self.getBasicDetails(request, id)
		self.SITE_DATA['page'] = 'property_settings'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property Settings'
		self.SITE_DATA['form_url'] = reverse('pssettings', args=[id])
		return render(request, 'property_settings.html', self.SITE_DATA)
	def post(self, request, id):
		try:
			pid= id
			pn = request.POST['pn']
			p = Property.objects.filter(id=pid).update(pname=pn)
			if p>0:
				data = {
					'status': 'success',
					'message': 'Property Successfully updated!',
				}
			else:
				data = {
					'status': 'error',
					'message': 'There was some error.',
				}
			return JsonResponse(data)
		except:
			return JsonResponse({
					'status': 'error',
					'message': 'There was some error. Please refresh and try again.',
				})
class PropertyPlatformsView(View, CMain):
	""" docstring for PropertyPlatformsView """
	def __init__(self, **arg):
		super(PropertyPlatformsView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		if(not self.valiDateProperty(request, id)):
			redirect('home')
		self.getBasicDetails(request, id)
		self.SITE_DATA['page'] = 'property_platforms'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property Platforms'
		self.SITE_DATA['form_url'] = reverse('psplatformweb', args=[id])
		pw = self.getPropertyWebDetails(request, id)
		if pw:
			self.SITE_DATA['website'] = pw
		return render(request, 'property_platforms.html', self.SITE_DATA)
class PropertyPlatformWebView(View, CMain):
	"""docstring for PropertyPlatformWebView"""
	def __init__(self, **arg):
		super(PropertyPlatformWebView, self).__init__()
		self.arg = arg
	def post(self, request, id):
		#data = {}
		pid= id
		pu = request.POST['pu']
		p = Property.objects.get(id=pid)
		if p:
			w = WebPlatform(properties=p, domain=pu, verify_code=get_random_string(length=6, allowed_chars='123456789abcdefghijklmnopqrstuvwxyz'))
			w.save()
			if w.properties_id:
				data = {
					'status': 'success',
					'message': 'Successfully saved!',
				}
		if not data:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)
class PropertyTrackingCodeView(View, CMain):
	""" docstring for PropertyTrackingCodeView """
	def __init__(self, **arg):
		super(PropertyTrackingCodeView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		if(not self.valiDateProperty(request, id)):
			redirect('home')
		self.getBasicDetails(request, id)
		self.SITE_DATA['page'] = 'property_trackingcode'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property Tracking Code'
		self.SITE_DATA['form_url'] = reverse('pstrackingcode', args=[id])
		return render(request, 'property_trackingcode.html', self.SITE_DATA)
class PropertyAPIKeysView(View, CMain):
	""" docstring for PropertyAPIKeysView """
	def __init__(self, **arg):
		super(PropertyAPIKeysView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		if(not self.valiDateProperty(request, id)):
			redirect('home')
		self.getBasicDetails(request, id)
		#pt = PropertyTokens.objects.filter(pid=id)
		self.SITE_DATA['page'] = 'property_apikeys'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property API Keys'
		self.SITE_DATA['form_url'] = reverse('psapikeys', args=[id])
		self.SITE_DATA['api_url_logs'] = reverse('psapikeylogs', args=[id])
		#self.SITE_DATA['token_logs'] = pt;
		return render(request, 'property_apikeys.html', self.SITE_DATA)
	def post(self, request, id):
		#data = {}
		pid= id
		p = Property.objects.get(id=pid)
		if p:
			cust_obj = self.getCustomerObj(request)
			secret_key = get_random_string(length=16)
			PropertyTokens.objects.filter(pid=pid).update(deleted_at=datetime.now())
			pt = PropertyTokens(pid=pid, psecret=make_password(secret_key), generated_by=cust_obj.id)
			pt.save()
			if pt.id:
				cp = CPRelationship.objects.filter(cust=cust_obj, prop=p)
				rc = dict(CPRelationship.ROLE_CHOICE)
				if not cust_obj.fname:
					gen_by = cust_obj.email
				else:
					gen_by = cust_obj.fname + ' ' + cust_obj.lname
				data = {
					'status': 'success',
					'message': 'Successfully saved!',
					'psecret': secret_key,
					'log': {
						'gen_by': gen_by,
						'role': rc[cp[0].role],
						'gen_time': pt.created_at
					}
				}
		if not data:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)
class PropertyAPIKeyLogsView(View, CMain):
	""" docstring for PropertyAPIKeyLogsView """
	def __init__(self, **arg):
		super(PropertyAPIKeyLogsView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		if(not self.valiDateProperty(request, id)):
			redirect('home')
		self.getBasicDetails(request, id)
		p = Property.objects.get(id=id)
		pt_objs = PropertyTokens.objects.filter(pid=id).order_by('created_at').reverse()
		dataTokens = {}
		if pt_objs:
			i = 0
			for pt in pt_objs:
				cust_obj = Customer.objects.get(id=pt.generated_by)
				if not cust_obj.fname:
					gen_by = cust_obj.email
				else:
					gen_by = cust_obj.fname + ' ' + cust_obj.lname
				cp = CPRelationship.objects.filter(cust=cust_obj, prop=p)
				rc = dict(CPRelationship.ROLE_CHOICE)
				dataTokens[i] = {
					'gen_by': gen_by,
					'role': rc[cp[0].role],
					'gen_time': pt.created_at,
				}
				i=i+1
		if pt:
			data = {
				'status': 'success',
				'logs': dataTokens,
			}
		if not data:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)
class PropertySDKView(View, CMain):
	"""docstring for PropertySDKView"""
	def __init__(self, **arg):
		super(PropertySDKView, self).__init__()
		self.arg = arg
	
	def get(self, request):
		self.SITE_DATA['page'] = 'property_sdk'
		self.SITE_DATA['page_title'] = 'Property SDK'
		self.SITE_DATA['form_url'] = reverse('propertySDK')
		return render(request, 'property_sdk.html', self.SITE_DATA)