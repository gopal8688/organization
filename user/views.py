from django.shortcuts import render

from django.views import View
from django.views.generic.base import RedirectView
from django.urls import reverse

from cmain.views import CMain
from auths.models import Customer,Property,CPRelationship,WebPlatform,PropertyTokens
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime

import json
import os

# Create your views here.
class UserView(View, CMain):
	"""docstring for UserView"""
	def __init__(self, **arg):
		super(UserView, self).__init__()
		self.arg = arg
	
	def get(self, request, pid):
		self.getBasicDetails(request, pid)
		self.SITE_DATA['page'] = 'userindex'
		self.SITE_DATA['page_menu'] = 'users'
		self.SITE_DATA['page_title'] = 'Users List Analytics'
		self.SITE_DATA['API_URLS'] = json.dumps({
			'rm':reverse('rm',args=[pid]),
			'ul':reverse('ul',args=[pid])
		})
		return render(request, 'userindex.html', self.SITE_DATA)

class UserDetailView(View, CMain):
	"""docstring for UserDetailView"""
	def __init__(self, **arg):
		super(UserDetailView, self).__init__()
		self.arg = arg

	def get(self, request, pid, username):
		self.getBasicDetails(request, pid)
		self.SITE_DATA['page'] = 'userdetail'
		self.SITE_DATA['page_menu'] = 'users'
		self.SITE_DATA['page_title'] = 'User Analytics'
		self.SITE_DATA['uid'] = username
		self.SITE_DATA['API_URLS'] = json.dumps({
			'bud':reverse('bud',args=[pid]),
			'lus':reverse('lus',args=[pid]),
			'rua':reverse('rua',args=[pid]),
			'ulo':reverse('ulo',args=[pid])
		})
		return render(request, 'userdetail.html', self.SITE_DATA)
		