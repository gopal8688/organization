from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from django.views import View
from django.views.generic.base import RedirectView

from cmain.views import CMain
from auths.models import Property       

# Create your views here.
class DashboardView(View, CMain):
    def __init__(self):
        CMain.__init__(self)
    

    @method_decorator(login_required)
    def get(self, request):
        self.getBasicDetails(request)
        self.SITE_DATA['page'] = 'dashboard'
        self.SITE_DATA['page_title'] = 'Dashboard'

        return render(request, 'home.html', self.SITE_DATA)

class PropertySelection(RedirectView):
    def get(self, request, id):
        #id = request.session['pid']
        print ('id', id)
        prop_obj = Property.objects.get(id=id)
        all_prop_obj = Property.objects.filter(properties__email=request.session['email'])
        
        context = {
            'rows': all_prop_obj,
            'cust_email': request.session['email'],
            'cust_full_name': request.session['cust_full_name'],
            'company': prop_obj.domain,
        }

        # Saving into session.
        request.session['pid'] = id
        
        #BaseView.SITE_DATA.update(context)
        return render(request, 'home.html', context)

    def get_redirect_url(self, request, *args, **kwargs):
        id = kwargs['id']
        prop_obj = Property.objects.get(id=id)
        all_prop_obj = Property.objects.filter(properties__email=request.session['email'])
        
        context = {
            'rows': all_prop_obj,
            'cust_email': request.session['email'],
            'cust_full_name': request.session['cust_full_name'],
            'company': prop_obj.domain,
        }

        # Saving into session.
        request.session['pid'] = id

        return super().get_redirect_url(*args, **kwargs)