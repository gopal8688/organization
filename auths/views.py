from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as ll, logout as signout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from cmain.views import CMain

# Create your views here.
def login(request):
    if request.session.get('email', None) and request.session.get('password', None):
        return redirect('home')
    return render(request, 'login.html')

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
        #return render(request, 'home.html')
        return redirect('home') #Redirect to 'home' url.

    else:
        return render(request, 'login.html', {'nopassword': '@@'})

def logout(request):
    signout(request)
    print ('session', request.session.keys())
    return HttpResponseRedirect('/')