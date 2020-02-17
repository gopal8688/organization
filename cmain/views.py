from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from auths.models import Customer, Property, CPRelationship, PropertyTokens
from base.views import BaseView

class CMain(BaseView):

    def __init__(self):
        BaseView.__init__(self)

    def getBasicDetails(self, request):
        email = request.session['email'] #.request.session['email']

        prop_obj = Property.objects.filter(properties__email=email)
        cust_obj = Customer.objects.get(email=email)

        cust_full_name = "%s %s"%(cust_obj.fname, cust_obj.lname)

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
        }
        
        # Saving into session.
        self.SITE_DATA.update(context)