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
	def get(self, request, id=0):

		#return HttpResponse(str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
		if((id>0) and (not self.valiDateProperty(request, id))):
			id=0

		if(id>0):
			self.SITE_DATA['page'] = 'dashboard'
			self.SITE_DATA['page_menu'] = 'home'
			self.SITE_DATA['page_title'] = 'Dashboard'
			# pprint(self.SITE_DATA['API_URLS'])
			self.SITE_DATA['API_URLS'] = json.dumps({
				'ds':reverse('ds',args=[id]),
				'hru':reverse('hru',args=[id]),
				'sa':reverse('sa',args=[id]),
				'la':reverse('la',args=[id]),
				'ura':reverse('ura',args=[id]),
				'rrd':reverse('rrd',args=[id])
			})
			# return redirect('propertyCreate')

			# pprint.pprint(self.SITE_DATA['API_URLS'])
			# return HttpResponse('')

			self.getBasicDetails(request, id)

			return render(request, 'home.html', self.SITE_DATA)
		else:
			self.setFirstProperty(request)
			if (request.session['pid']==0):
				return redirect('propertyCreate')
			else:
				return redirect('pr-home',request.session['pid'])
