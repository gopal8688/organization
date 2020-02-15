from django.urls import include, path

from .views import DashboardView as DV

urlpatterns = [
    path('', DV.as_view(), name='home'),
    #path('', PS.as_view(), name='prop_select'),
]