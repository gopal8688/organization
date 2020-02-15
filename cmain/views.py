from django.shortcuts import render, redirect
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login as ll, logout as signout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views import View

from auths.models import Customer, Property, CPRelationship, PropertyTokens
from base.views import BaseView

class CMain(BaseView):

    #@login_required
    def getBasicDetails(self, request):
        email = request.session['email']

        prop_obj = Property.objects.filter(properties__email=email)
        cust_obj = Customer.objects.get(email=email)

        cust_full_name = "%s %s"%(cust_obj.fname, cust_obj.lname)

        if prop_obj is not None:
            request.session['pid'] = prop_obj[0].id
        else:
            return HttpResponse('The user has not properties to show.')

        context = {
            'rows': prop_obj,
            'cust_email': cust_obj.email,
            'cust_full_name': cust_full_name,
            'company': prop_obj[0].domain,
            'request': request,
            'show_row': prop_obj[0],
        }

        # Saving into session.
        request.session['cust_full_name'] = cust_full_name

        return context
        #BaseView.SITE_DATA.update(context)
        #return render(request, 'home.html', context)

    def selectPropertyID(self, request):
        id = request.session['pid']
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
        
        return context
        #BaseView.SITE_DATA.update(context)
        #return render(request, 'home.html', context)

