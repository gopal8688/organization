from django.shortcuts import render

# Create your views here.
def view(request):
    print ('ENTERED>>>>>>>>>>>>>>>')
    return render(request, 'home.html')