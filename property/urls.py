from django.urls import include, path

from .views import PropertyCreateView as PV,PropertyPlatformsView,PropertyTrackingCodeView,PropertyAPIKeysView

urlpatterns = [
	path('create', PV.as_view(), name="propertyCreate"),
	path('settings/platforms/<int:id>', PropertyPlatformsView.as_view(), name="psplatforms"),
	path('settings/tracking-code/<int:id>', PropertyTrackingCodeView.as_view(), name="pstrackingcode"),
	path('settings/api-keys/<int:id>', PropertyAPIKeysView.as_view(), name="psapikeys")
]