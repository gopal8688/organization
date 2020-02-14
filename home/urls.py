# Django libraries.
from django.contrib import admin
from django.urls import include, path

# Django files.
from . import views

urlpatterns = [
    path('/', views.view, name='home'),
]