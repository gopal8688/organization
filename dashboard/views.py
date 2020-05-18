from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from django.views import View
from django.views.generic.base import RedirectView
from django.urls import reverse
from datetime import datetime, timedelta

from cmain.views import CMain
from auths.models import Property
from django.http import HttpResponse, JsonResponse
from django.core import serializers

import json
import os

# Create your views here.
class DashboardView(View, CMain):
	def __init__(self):
		CMain.__init__(self)


	@method_decorator(login_required)
	def get(self, request, uuid=''):

		#return HttpResponse(str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
		if((uuid!='') and (not self.valiDateProperty(request, uuid))):
			uuid=''

		if(uuid!=''):
			prop_obj = Property.objects.get(uuid=uuid)
			self.SITE_DATA['page'] = 'dashboard'
			self.SITE_DATA['page_menu'] = 'home'
			self.SITE_DATA['page_title'] = 'Dashboard'
			# pprint(self.SITE_DATA['API_URLS'])
			self.SITE_DATA['API_URLS'] = json.dumps({
				'ds':reverse('ds',args=[prop_obj.id]),
				'hru':reverse('hru',args=[prop_obj.id]),
				'sa':reverse('sa',args=[prop_obj.id]),
				'la':reverse('la',args=[prop_obj.id]),
				'ura':reverse('ura',args=[prop_obj.id]),
				'rrd':reverse('rrd',args=[prop_obj.id])
			})
			# return redirect('propertyCreate')

			# pprint.pprint(self.SITE_DATA['API_URLS'])
			# return HttpResponse('')

			self.getBasicDetails(request, uuid)

			return render(request, 'home.html', self.SITE_DATA)
		else:
			self.setFirstProperty(request)
			if (request.session['pid']==0):
				return redirect('propertyCreate')
			else:
				return redirect('pr-home',request.session['uuid'])
