from django.urls import include, path

from .views import PropertyCreateView as PV,PropertySDKView,PropertySettingsView,PropertyPlatformsView,PropertyPlatformWebView,PropertyTrackingCodeView,PropertyAPIKeysView,PropertyAPIKeyLogsView

urlpatterns = [
	path('create', PV.as_view(), name="propertyCreate"),
	path('sdk', PropertySDKView.as_view(), name="propertySDK"),
	path('settings/<int:id>', PropertySettingsView.as_view(), name="pssettings"),
	path('settings/platforms/<int:id>', PropertyPlatformsView.as_view(), name="psplatforms"),
	path('settings/platforms/<int:id>/website', PropertyPlatformWebView.as_view(), name="psplatformweb"),
	path('settings/tracking-code/<int:id>', PropertyTrackingCodeView.as_view(), name="pstrackingcode"),
	path('settings/api-keys/<int:id>', PropertyAPIKeysView.as_view(), name="psapikeys"),
	path('settings/api-key-logs/<int:id>', PropertyAPIKeyLogsView.as_view(), name="psapikeylogs")
]