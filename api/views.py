from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from django.views import View
from django.views.generic.base import RedirectView
from django.urls import reverse
from datetime import datetime, timedelta

from api.forms import HighRiskUsersForm,DashboardStatsForm,SecurityAlertsForm,LoginAttemptsForm,UserRiskAnalyticsForm,RegionRiskForm,RiskMapForm,UsersListForm,BasicUserDetailsForm,UserDetailsLimitForm

from cmain.views import CMain
from auths.models import Property
from django.http import HttpResponse, JsonResponse

from pymongo import MongoClient
from api.customer_apis.config import Config
from api.customer_apis.highrisk import HighRiskUsers
from api.customer_apis.stats import DashboardStats
from api.customer_apis.security_alerts import SecurityAlerts
from api.customer_apis.login_attempts import LoginAttempts
from api.customer_apis.user_risk_analytics import UserRiskAnalytics
from api.customer_apis.region_risk import RegionRiskCount
from api.customer_apis.user_info import UsersInfo
from api.customer_apis.user_details import UserDetails

import json
import os

class DashboardStatsView(View, CMain, DashboardStats):
	"""docstring for DashboardStatsView"""
	def __init__(self, **arg):
		super(DashboardStatsView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyDSForm = DashboardStatsForm(request.GET)
		if MyDSForm.is_valid():
			duration = MyDSForm.cleaned_data['dur']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getCounts(str(id), from_date, to_date)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class HighRiskUsersView(View, CMain, HighRiskUsers):
	"""docstring for HighRiskUsersView"""
	def __init__(self, **arg):
		super(HighRiskUsersView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyHRUForm = HighRiskUsersForm(request.GET)
		if MyHRUForm.is_valid():
			duration = MyHRUForm.cleaned_data['dur']
			limit = MyHRUForm.cleaned_data['limit']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getHighRiskUsers(str(id), limit, from_date, to_date)
			if data['status'] == 'success':
				data['user_url'] = reverse('userdetail',args=[id,1])[0:-2]
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class SecurityAlertsView(View, CMain, SecurityAlerts):
	"""docstring for SecurityAlertsView"""
	def __init__(self, **arg):
		super(SecurityAlertsView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MySAForm = SecurityAlertsForm(request.GET)
		if MySAForm.is_valid():
			duration = MySAForm.cleaned_data['dur']
			limit = MySAForm.cleaned_data['limit']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getNotableDevice(str(id), limit, from_date, to_date)
			if data['status'] == 'success':
				data['user_url'] = reverse('userdetail',args=[id,1])[0:-2]
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class LoginAttemptsView(View, CMain, LoginAttempts):
	"""docstring for LoginAttemptsView"""
	def __init__(self, **arg):
		super(LoginAttemptsView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyLAForm = LoginAttemptsForm(request.GET)
		if MyLAForm.is_valid():
			duration = MyLAForm.cleaned_data['dur']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getLogInAttempts(str(id), from_date, to_date)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class UserRiskAnalyticsView(View, CMain, UserRiskAnalytics):
	"""docstring for UserRiskAnalyticsView"""
	def __init__(self, **arg):
		super(UserRiskAnalyticsView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyURAForm = UserRiskAnalyticsForm(request.GET)
		if MyURAForm.is_valid():
			duration = MyURAForm.cleaned_data['dur']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getLogScore(str(id), from_date, to_date)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class RegionRiskDistView(View, CMain, RegionRiskCount):
	"""docstring for RegionRiskDistView"""
	def __init__(self, **arg):
		super(RegionRiskDistView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyRRForm = RegionRiskForm(request.GET)
		if MyRRForm.is_valid():
			duration = MyRRForm.cleaned_data['dur']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getCountryRisk(str(id), from_date, to_date)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class RiskMapView(View, CMain, UsersInfo):
	"""docstring for RiskMapView"""
	def __init__(self, **arg):
		super(RiskMapView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyForm = RiskMapForm(request.GET)
		if MyForm.is_valid():
			duration = MyForm.cleaned_data['dur']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getRiskMap(str(id), from_date, to_date)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class UsersListView(View, CMain, UsersInfo):
	"""docstring for UsersListView"""
	def __init__(self, **arg):
		super(UsersListView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyForm = UsersListForm(request.GET)
		if MyForm.is_valid():
			duration = MyForm.cleaned_data['dur']
			limit = MyForm.cleaned_data['limit']
			duration = duration.split(":")
			from_date = duration[0]
			to_date = duration[1]
			from_date = datetime.strptime(from_date, '%d-%m-%Y')
			to_date = datetime.strptime(to_date, '%d-%m-%Y')
			data = self.getUserList(str(id), from_date, to_date)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class BasicUserDetailsView(View, CMain, UserDetails):
	"""docstring for BasicUserDetailsView"""
	def __init__(self, **arg):
		super(BasicUserDetailsView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyForm = BasicUserDetailsForm(request.GET)
		if MyForm.is_valid():
			user = MyForm.cleaned_data['user']
			data = self.getBasicUserDetails(str(id), user)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class LinkedUsersView(View, CMain, UserDetails):
	"""docstring for LinkedUsersView"""
	def __init__(self, **arg):
		super(LinkedUsersView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyForm = UserDetailsLimitForm(request.GET)
		if MyForm.is_valid():
			user = MyForm.cleaned_data['user']
			limit = MyForm.cleaned_data['limit']
			data = self.getLinkedUsers(str(id), user, limit)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class RecentUserActivitiesView(View, CMain, UserDetails):
	"""docstring for RecentUserActivitiesView"""
	def __init__(self, **arg):
		super(RecentUserActivitiesView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyForm = UserDetailsLimitForm(request.GET)
		if MyForm.is_valid():
			user = MyForm.cleaned_data['user']
			limit = MyForm.cleaned_data['limit']
			data = self.getRecentActivities(str(id), user, limit)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)

class UserLocationsView(View, CMain, UserDetails):
	"""docstring for UserLocationsView"""
	def __init__(self, **arg):
		super(UserLocationsView, self).__init__()
		self.arg = arg
	
	def get(self, request, id):
		MyForm = BasicUserDetailsForm(request.GET)
		if MyForm.is_valid():
			user = MyForm.cleaned_data['user']
			data = self.getUserLocations(str(id), user)
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data, status=200)