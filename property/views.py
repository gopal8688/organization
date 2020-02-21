from django.shortcuts import render
from django.utils.crypto import get_random_string

from django.views import View
from django.views.generic.base import RedirectView
from django.urls import reverse

from cmain.views import CMain
from auths.models import Customer,Property,CPRelationship
from django.http import HttpResponse, JsonResponse
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
					'pid': p.id,
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
		self.SITE_DATA['page'] = 'propertyplatforms'
		self.SITE_DATA['page_title'] = 'Property Platforms'
		self.SITE_DATA['form_url'] = reverse('psplatforms')
		return render(request, 'property_platforms.html', self.SITE_DATA)
class PropertyTrackingCodeView(View, CMain):
	""" docstring for PropertyTrackingCodeView """
	def __init__(self, **arg):
		super(PropertyTrackingCodeView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		self.SITE_DATA['page'] = 'propertytrackingcode'
		self.SITE_DATA['page_title'] = 'Property Tracking Code'
		self.SITE_DATA['form_url'] = reverse('pstrackingcode')
		return render(request, 'property_trackingcode.html', self.SITE_DATA)
class PropertyAPIKeysView(View, CMain):
	""" docstring for PropertyAPIKeysView """
	def __init__(self, **arg):
		super(PropertyAPIKeysView, self).__init__()
		self.arg = arg
	def get(self, request, id):
		self.SITE_DATA['page'] = 'propertyapikeys'
		self.SITE_DATA['page_title'] = 'Property API Keys'
		self.SITE_DATA['form_url'] = reverse('psapikeys')
		return render(request, 'property_apikeys.html', self.SITE_DATA)