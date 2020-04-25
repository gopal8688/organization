from django.urls import include, path
from django.contrib.auth.decorators import login_required
from .views import ProfileView as PV, ProfilePersonal,ProfilePassword,ProfileCompany

urlpatterns = [
    path('', login_required(PV.as_view()), name='view'),
    path('personal', login_required(ProfilePersonal.as_view()), name='profilePersonal'),
    path('password', login_required(ProfilePassword.as_view()), name='profilePassword'),
    path('company', login_required(ProfileCompany.as_view()), name='profileCompany')
]