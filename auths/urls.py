# Django libraries.
from django.urls import include, path

# Django files.
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('auth/', views.loginCheck, name='login_check'),
    path('logout', views.logout, name='logout'),
]