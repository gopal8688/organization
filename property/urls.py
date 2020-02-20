from django.urls import include, path

from .views import PropertyView as PV

urlpatterns = [
	path('create', PV.as_view(), name="propertyCreate")
];