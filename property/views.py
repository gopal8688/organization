from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from django.views import View
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from cmain.views import CMain
from auths.models import Customer,Property,CPRelationship,WebPlatform,PropertyTokens,DoNotTrackIP,DoNotTrackEmail,CustomizeAlerts,Webhooks
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime
from property.forms import *

import os
import re
import sys
import json
import uuid


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
			# track = request.POST['track']
			p = Property(pid=get_random_string(length=16, allowed_chars='123456789'),uuid = uuid.uuid1(),pname = pn)
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

	def uuid(self):
		try:
			count=Property.objects.all().count()
			for i in range(1, count):
				q=Property.objects.get(id=i)
				if (q.uuid==''):
					query=Property.objects.filter(id=i).update(uuid=uuid.uuid1())
					if query>0:
						data = {
						'status': 'success',
						'message': 'Property Successfully updated!',
						}
					else:
						data = {
						'status': 'error',
						'message': 'There was some error.',
						}

				else:
					data = {
						'status': 'success',
						'message': 'Nothing to update!',
						}
				i=i+1
				
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
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
		# if(not self.getBasicDetails(request, id)):
		# 	redirect('home')
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
			track = request.POST['track']
			if(track=='true'):
				track=1
			else:
				track=0
			p = Property.objects.filter(id=pid).update(pname=pn, track=track)
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
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
		#return HttpResponse(str(request.GET['firstime']))
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
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
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
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
		self.getBasicDetails(request, id)
		#pt = PropertyTokens.objects.filter(pid=id)
		self.SITE_DATA['page'] = 'property_apikeys'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property API Keys'
		self.SITE_DATA['form_url'] = reverse('psapikeys', args=[id])
		self.SITE_DATA['api_url_logs'] = reverse('psapikeylogs', args=[id])
		#self.SITE_DATA['password'] = make_password("kN0Hugme46cfRVfl","z8Mnhff89sE0")
		#self.SITE_DATA['token_logs'] = pt;
		return render(request, 'property_apikeys.html', self.SITE_DATA)
	def post(self, request, id):
		#data = {}
		# pid= id
		# p = Property.objects.get(id=pid)
		p = Property.objects.get(id=id)
		pid = p.pid
		cust_obj = self.getCustomerObj(request)
		
		secret_key = get_random_string(length=16)
		secret_key_hashed = make_password(secret_key)
		generated_by = cust_obj.id

		try:
			pt_obj = PropertyTokens.objects.get(pid=pid, deleted_at__isnull=True)
			pt_obj.deleted_at=datetime.now()
			pt_obj.save()

			pt = PropertyTokens(
				pid=pid,
				psecret=secret_key_hashed,
				generated_by=generated_by
			)
		except PropertyTokens.DoesNotExist:
			#print ('HERE')
			pt_obj = PropertyTokens(
				pid=pid,
				psecret=secret_key_hashed,
				generated_by=generated_by,
			)
		pt.save()
		try:
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
		except:
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
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
		self.getBasicDetails(request, id)
		p = Property.objects.get(id=id)
		pt_objs = PropertyTokens.objects.filter(pid=p.pid).order_by('created_at').reverse()
		dataTokens = {}
		try:
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
			data = {
				'status': 'success',
				'logs': dataTokens,
			}
		except:
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
class PropertyDNTrackView(View, CMain):
	""" docstring for PropertyDNTrackView """
	def __init__(self, **arg):
		super(PropertyDNTrackView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
		# if(not self.getBasicDetails(request, id)):
		# 	redirect('home')
		self.getBasicDetails(request, id)
		self.SITE_DATA['page'] = 'property_dntrack'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property Settings'
		self.SITE_DATA['form_url_ip'] = reverse('psdntrackip', args=[id])
		self.SITE_DATA['form_url_email'] = reverse('psdntrackemail', args=[id])
		return render(request, 'property_dntrack.html', self.SITE_DATA)

class PropertyDNTrackIPView(View, CMain):
	""" docstring for PropertyDNTrackIPView """
	def __init__(self, **arg):
		super(PropertyDNTrackIPView, self).__init__()
		self.arg = arg

	def get(self, request, id):
		self.getBasicDetails(request, id)
		#p = DoNotTrackIP.objects.get(id=id)
		try:
			pt_objs = DoNotTrackIP.objects.filter(pid=id).order_by('created_at').reverse()
			dataTokens = []
			if pt_objs:
				i = 0
				for pt in pt_objs:
					dataTokenItem = {}
					dataTokenItem['id'] = pt.id
					dataTokenItem['ip'] = pt.ip
					dataTokens.append(dataTokenItem)
					i=i+1
			data = {
				'status': 'success',
				'logs': dataTokens,
			}
		except:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)
		

	def post(self, request, id):
		try:
			self.getBasicDetails(request, id)
			prop_obj = self.getPropertyObj(request)
			# Form submission code goes here
			dnt_ip = request.POST['dnt_ip']
			ipRegex = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
			ipRangeRegex = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/([0-9]|[1-2][0-9]|3[0-2])$'
			# Comma separated entries will be broken and added separately
			if((re.search(ipRegex, dnt_ip))):
				q = DoNotTrackIP(prop = prop_obj, ip = dnt_ip)
				q.save()
				data = {
				'status': 'success',
				'message': 'IP address successfully added for not tracking.',
				'data': {'id':q.id,'ip':q.ip},
				}
			elif((re.search(ipRangeRegex, dnt_ip))):
				q = DoNotTrackIP(prop = prop_obj, ip = dnt_ip)
				q.save()
				data = {
				'status': 'success',
				'message': 'IP range successfully added for not tracking.',
				'data': {'id':q.id,'ip':q.ip},
				}
			else:
				data = {
				'status': 'error',
				'message': 'Please enter valid IP address or IP range'
				}
		except:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)
	def delete(self, request, id):
		try:
			ip_obj = DoNotTrackIP.objects.get(id=id)
			self.getBasicDetails(request, ip_obj.pid)
			DoNotTrackIP.objects.filter(id=id).delete()
			data = {
					'status': 'success',
					'message': 'IP address successfully removed',
					#'data': ip_id,
					}
		except:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)

class PropertyDNTrackEmailView(View, CMain):
	""" docstring for PropertyDNTrackEmailView """
	def __init__(self, **arg):
		super(PropertyDNTrackEmailView, self).__init__()
		self.arg = arg

	def get(self, request, id):
		self.getBasicDetails(request, id)
		#p = DoNotTrackEmail.objects.get(id=id)
		pt_objs = DoNotTrackEmail.objects.filter(pid=id).order_by('created_at').reverse()
		dataTokens = []
		try:
			pt_objs = DoNotTrackEmail.objects.filter(pid=id).order_by('created_at').reverse()
			dataTokens = []
			if pt_objs:
				i = 0
				for pt in pt_objs:
					dataTokenItem = {}
					dataTokenItem['id'] = pt.id
					dataTokenItem['email'] = pt.email
					dataTokens.append(dataTokenItem)
					i=i+1
			data = {
				'status': 'success',
				'logs': dataTokens,
			}
		except:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)

	def post(self, request, id):
		try:
			self.getBasicDetails(request, id)
			prop_obj = self.getPropertyObj(request)
			# Form submission code goes here
			email = request.POST['dnt_email']
			#check for valid email id or domain name
			emailRegex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
			domainRegex = "\A([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\Z"
			if((re.search(emailRegex, email))):
				q = DoNotTrackEmail(prop = prop_obj, email = email)
				q.save()
				data = {
				'status': 'success',
				'message': 'Email successfully added for not tracking.',
				'data': {'id':q.id,'email':q.email},
				}
			elif((re.search(domainRegex, email))):
				q = DoNotTrackEmail(prop = prop_obj, email = email)
				q.save()
				data = {
				'status': 'success',
				'message': 'Domain successfully added for not tracking.',
				'data': {'id':q.id,'email':q.email},
				}
			else:
				data = {
				'status': 'error',
				'message': 'Please enter valid email address or domain name'
				}

		except:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)
	def delete(self, request, id):
		try:
			email_obj = DoNotTrackEmail.objects.get(id=id)
			self.getBasicDetails(request, email_obj.pid)
			DoNotTrackEmail.objects.filter(id=id).delete()
			data = {
					'status': 'success',
					'message': 'Email successfully removed',
					#'data': ip_id,
					}
		except:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)
		
class PropertyWebhooksView(View, CMain):
	""" docstring for PropertyWebhooksView """
	def __init__(self, **arg):
		super(PropertyWebhooksView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
		# if(not self.getBasicDetails(request, id)):
		# 	redirect('home')
		self.getBasicDetails(request, id)
		self.SITE_DATA['page'] = 'property_webhooks'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property Settings'
		self.SITE_DATA['form_url'] = reverse('pswebhooks', args=[id])
		return render(request, 'property_webhooks.html', self.SITE_DATA)
	def post(self, request, id):
		try:
			self.getBasicDetails(request, id)
			prop_obj = self.getPropertyObj(request)
			# Form submission code goes here
			url = request.POST['url']
			options = request.POST['options']
			is_active = request.POST['is_active']
			if(is_active==True):
				is_active = 1
			else:
				is_active = 0

			#check for valid url
			urlRegex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
			
			if((re.search(urlRegex, url))):
				q = Webhooks(prop = prop_obj, url = url, options = options, is_active = is_active)
				q.save()
				data = {
					'status': 'success',
					'message': 'URL successfully added for webhook.',
					'data': {'id':q.id,'url':q.url, 'options':q.options, 'is_active':q.is_active},
				}
			else:
				data = {
					'status': 'error',
					'message': 'Please enter valid URL'
				}

		except:
			data = {
				'status': 'error',
				'message': 'There was some error.',
			}
		return JsonResponse(data)


class PropertyCAlertsView(View, CMain):
	""" docstring for PropertyCAlertsView """
	def __init__(self, **arg):
		super(PropertyCAlertsView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		# if(not self.valiDateProperty(request, id)):
		# 	redirect('home')
		# if(not self.getBasicDetails(request, id)):
		# 	redirect('home')
		self.getBasicDetails(request, id)
		prop_obj = self.getPropertyObj(request)
		self.SITE_DATA['email_active'] = 0
		co_obj = CustomizeAlerts.objects.filter(prop=prop_obj, app_type= 'email')
		if co_obj:
			self.SITE_DATA['email_active'] = 1
			self.SITE_DATA['co_obj'] = co_obj[0]
		self.SITE_DATA['page'] = 'property_calerts'
		self.SITE_DATA['page_menu'] = 'settings'
		self.SITE_DATA['page_title'] = 'Property Settings'
		self.SITE_DATA['form_url'] = reverse('pscalerts', args=[id])
		return render(request, 'property_calerts.html', self.SITE_DATA)

	def post(self, request, id):
		#try:
		self.getBasicDetails(request, id)
		prop_obj = self.getPropertyObj(request)
		# Form submission code goes here
		risk_threshold = request.POST['risk_threshold']
		app_uid = request.POST['username']
		is_active = request.POST['track']

		#check for valid email id
		emailRegex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		
		if((re.search(emailRegex, app_uid))):
			co_obj = CustomizeAlerts.objects.filter(prop = prop_obj, app_type = 'email')
			if not co_obj:
				q = CustomizeAlerts(prop = prop_obj, risk_threshold=risk_threshold, app_uid = app_uid, app_type= 'email', is_active= is_active)
				q.save()
				dataReturn = {'id':q.id,'app_uid':q.app_uid, 'risk_threshold':q.risk_threshold, 'is_active': q.is_active}
			else:
				co_obj.update(prop = prop_obj, risk_threshold=risk_threshold, app_uid = app_uid, app_type= 'email', is_active= is_active)
				dataReturn = {'id':co_obj[0].id,'app_uid':co_obj[0].app_uid, 'risk_threshold':co_obj[0].risk_threshold, 'is_active': co_obj[0].is_active}
			data = {
			'status': 'success',
			'message': 'Email and risk threshold successfully added.',
			'data': dataReturn,
			}
		else:
			data = {
			'status': 'error',
			'message': 'Please enter valid email address'
			}
		# except:
		# 	data = {
		# 		'status': 'error',
		# 		'message': 'There was some error.',
		# 	}
		return JsonResponse(data)

