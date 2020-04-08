from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
#from django.conf.urls.static import static

from cmain.views import CMain
from auths.models import Customer
from cprof.forms import CompanyForm

# Create your views here.
class ProfileView(View, CMain):
	def get(self, request):
		cust_obj = self.getCustomerObj(request)
		self.SITE_DATA['page'] = 'personal'
		self.SITE_DATA['page_menu'] = 'personal'
		self.SITE_DATA['page_title'] = 'Personal Information'
		self.SITE_DATA['cust_obj'] = cust_obj
		self.SITE_DATA['form_url_personal'] = reverse('profilePersonal')
		self.SITE_DATA['form_url_password'] = reverse('profilePassword')
		self.SITE_DATA['form_url_company'] = reverse('profileCompany')

		return render(request, 'personal.html', self.SITE_DATA)

class ProfilePersonal(View, CMain):
	def post(self, request):
		try:
			cust_obj = self.getCustomerObj(request)
			cust_obj.fname = request.POST['first_name']
			cust_obj.lname = request.POST['last_name']
			cust_obj.email = request.POST['cemail']
			cust_obj.phone = request.POST['cphone']
			cust_obj.sex = request.POST['sex']
			cust_obj.save(update_fields=['fname','lname','email','phone','sex'])

			data = {
				'status': 'success'
			}
			return JsonResponse(data)
		except:
			return JsonResponse({
					'status': 'error',
					'message': 'There was some error. Please refresh and try again.',
				})

class ProfilePassword(View, CMain):
	def post(self, request):
		try:
			if (request.POST['password'] == request.POST['cpassword']):
				cust_obj = self.getCustomerObj(request)
				cust_obj.password = make_password(request.POST['password'])
				cust_obj.save(update_fields=['password'])

				data = {
					'status': 'success'
				}
			else:
				data = {
					'status': 'error',
					'message': 'Passwords do not match.',
				}
			return JsonResponse(data)
		except:
			return JsonResponse({
					'status': 'error',
					'message': 'There was some error. Please refresh and try again.',
				})

class ProfileCompany(View, CMain):
	def post(self, request):
		MyCompanyForm = CompanyForm(request.POST, request.FILES)
		if MyCompanyForm.is_valid():
			cust_obj = self.getCustomerObj(request)
			cust_obj.org_name = MyCompanyForm.cleaned_data['org_name']
			cust_obj.brand_name = MyCompanyForm.cleaned_data['brand_name']
			cust_obj.brand_url = MyCompanyForm.cleaned_data['brand_url']
			if MyCompanyForm.cleaned_data['brand_logo']:
				cust_obj.brand_logo = MyCompanyForm.cleaned_data['brand_logo']			
			cust_obj.save()
			data = {
				'status': 'success'
			}
		else:
			data = {
				'status': 'error',
				'message': 'There was some error. Please refresh and try again.'
			}
		return JsonResponse(data)
		#try:
		# cust_obj = self.getCustomerObj(request)
		# cust_obj.org_name = request.POST['company_name']
		# cust_obj.brand_name = request.POST['brand_name']
		# cust_obj.brand_url = request.POST['brand_url']

		# brand_logo = request.FILES['brand_logo']
		# if brand_logo:
		# 	cust_obj.brand_logo = default_storage.save(static('brand_logo/'+brand_logo.name), brand_logo)
		# 	cust_obj.save(update_fields=['org_name','brand_name','brand_url','brand_logo'])
		# else:
		# 	cust_obj.save(update_fields=['org_name','brand_name','brand_url'])

		# data = {
		# 	'status': 'success'
		# }
		# return JsonResponse(data)
		# except:
		# 	return JsonResponse({
		# 			'status': 'error',
		# 			'message': 'There was some error. Please refresh and try again.',
		# 		})