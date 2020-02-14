from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as ll, logout as signout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from .models import Customer, Property, CPRelationship, PropertyTokens

# Create your views here.
def login(request):
    #if request.session.get('email', None) and request.session.get('password', None):
     #   return redirect(home)
    return render(request, 'login.html')

#@login_required
def loginCheck(request):
    if not request.session.get('email', None) and not request.session.get('password', None):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        already_authenticated = False
    else:
        already_authenticated = True
    
    if already_authenticated or (user is not None and user.is_active):

        # Saving into session        
        if not already_authenticated:
            ll(request, user)  
            request.session['email'] = email
            request.session['password'] = password
        
        return redirect(home)
    else:
        return render(request, 'login.html')

def logout(request):
    signout(request)
    return HttpResponseRedirect('login')

@login_required
def home(request):
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

    return render(request, 'home.html', context)

def selectProperty(request):
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
    
    return render(request, 'home.html', context)
