from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from auths.models import Customer, Property, CPRelationship, PropertyTokens
from base.views import BaseView

class CMain(BaseView):

    def __init__(self):
        BaseView.__init__(self)
    
    def getAbsoluteURL(self, request):
        full_url = request.get_host()
        is_https = request.is_secure()
        
        if is_https:
            full_url = "https://%s/"%full_url
        else:
            full_url = "http://%s/"%full_url

        return full_url

    def getBasicDetails(self, request):
        email = request.session['email'] #.request.session['email']

        prop_obj = Property.objects.filter(properties__email=email)
        cust_obj = Customer.objects.get(email=email)

        cust_full_name = "%s %s"%(cust_obj.fname, cust_obj.lname)
        #print ('JSONss', self.SITE_DATA['API_URLS'])
        if prop_obj is not None:
            request.session['pid'] = prop_obj[0].id
        else:
            request.session['pid'] = 0
            
        context = {
            'rows': prop_obj,
            'cust_email': cust_obj.email,
            'cust_full_name': cust_full_name,
            'company': prop_obj[0].domain,
            'request': request,
            'show_row': prop_obj[0],
            'base_url': self.getAbsoluteURL(request),
            'pid': request.session['pid'],
            'API_KEY': 'eiWee8ep9due4deeshoa8Peichai8Eih',
        }
        
        # Saving into session.
        self.SITE_DATA.update(context)