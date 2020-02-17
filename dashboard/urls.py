from django.urls import include, path

from .views import DashboardView as DV, PropertySelection as PS

urlpatterns = [
    path('', DV.as_view(), name='home'),
    path('<int:id>', PS.as_view(), name='prop_select'),
]