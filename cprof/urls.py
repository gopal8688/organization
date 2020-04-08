from django.urls import include, path

from .views import ProfileView as PV, ProfilePersonal,ProfilePassword,ProfileCompany

urlpatterns = [
    path('', PV.as_view(), name='view'),
    path('personal', ProfilePersonal.as_view(), name='profilePersonal'),
    path('password', ProfilePassword.as_view(), name='profilePassword'),
    path('company', ProfileCompany.as_view(), name='profileCompany')
]