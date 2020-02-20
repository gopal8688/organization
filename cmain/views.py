from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from auths.models import Customer, Property, CPRelationship, PropertyTokens
from base.views import BaseView
from django.http import HttpResponse

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
        
        cust_obj = Customer.objects.get(email=email)

        cust_full_name = "%s %s"%(cust_obj.fname, cust_obj.lname)
        #print ('JSONss', self.SITE_DATA['API_URLS'])

        context = {
            'cust_email': cust_obj.email,
            'cust_full_name': cust_full_name,
            'request': request,
            'base_url': self.getAbsoluteURL(request),
            'API_KEY': 'eiWee8ep9due4deeshoa8Peichai8Eih',
        }

        prop_obj = Property.objects.filter(properties__email=email)

        if not prop_obj:
            # if self.SITE_DATA['page'] is not 'create_property':
            #     return redirect
            request.session['pid'] = 12
            context.update({
                'pid': request.session['pid'],
            })
        else:
            request.session['pid'] = prop_obj[0].id
            context.update({
                'rows': prop_obj,
                'show_row': prop_obj[0],
                'company': prop_obj[0].domain,
                'pid': request.session['pid'],
            })

        # print(request.session['pid'])
        # return str(request.session['pid'])
            
        
        
        # Saving into session.
        self.SITE_DATA.update(context)