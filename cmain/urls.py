# Django libraries.
from django.contrib import admin
from django.urls import include, path

# Django files.
from .views import CMain, PropertySelection

urlpatterns = [
    #path('', CMain.as_view(), name='home'),
    #path('', PropertySelection.as_view(), name='prop_select'),
]