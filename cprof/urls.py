from django.urls import include, path

from .views import ProfileView as PV

urlpatterns = [
    path('', PV.as_view(), name='view'),
]