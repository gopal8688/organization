"""admin_dboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django libraries.
from django.contrib import admin
from django.urls import include, path

# Django files.
from . import views

# URLs
urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.logout, name='logout'),
    path('auth/', views.loginCheck, name='login_check'),
    path('home/', views.home, name='home'),
    path('home/', views.selectProperty, name='prop_select'),
    #path('home/', include('home.urls')),
    path('admin/', admin.site.urls),
]
