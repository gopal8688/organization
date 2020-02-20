from django.shortcuts import render

from django.views import View
from django.views.generic.base import RedirectView

from cmain.views import CMain
from auths.models import Property
from django.http import HttpResponse
import os

# Create your views here.
class PropertyView(View, CMain):
	"""docstring for PropertyView"""
	def __init__(self, **arg):
		super(PropertyView, self).__init__()
		self.arg = arg
	def get(self, request):
		self.SITE_DATA['page'] = 'property_create'
		self.SITE_DATA['page_title'] = 'Create Property'

		return render(request, 'property_create.html', self.SITE_DATA);
		