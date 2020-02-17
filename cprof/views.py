from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render
from django.views import View

from cmain.views import CMain
from auths.models import Customer

# Create your views here.
class ProfileView(View, CMain):
    def get(self, request):
        self.SITE_DATA['page'] = 'personal'
        self.SITE_DATA['page_title'] = 'Personal'
        
        return render(request, 'personal.html', self.SITE_DATA)

class ProfileUpdate(View, CMain):
    def post(self, request):
        cobj = Customer.objects.get(email=CMain.SITE_DATA['email'])
        #request.POST['']