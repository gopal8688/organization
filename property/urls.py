from django.urls import include, path
from django.contrib.auth.decorators import login_required
from .views import PropertyCreateView as PV, PropertySDKView, PropertySettingsView, PropertyPlatformsView, PropertyPlatformWebView, PropertyTrackingCodeView, PropertyAPIKeysView, PropertyAPIKeyLogsView, PropertyDNTrackView, PropertyWebhooksView, PropertyCAlertsView, PropertyDNTrackIPView, PropertyDNTrackIPDeleteView, PropertyDNTrackEmailView, PropertyDNTrackEmailDeleteView

urlpatterns = [
	path('create', login_required(PV.as_view()), name="propertyCreate"),
	path('sdk', login_required(PropertySDKView.as_view()), name="propertySDK"),
	path('settings/<str:uuid>', login_required(PropertySettingsView.as_view()), name="pssettings"),
	path('settings/platforms/<str:uuid>', login_required(PropertyPlatformsView.as_view()), name="psplatforms"),
	path('settings/platforms/<int:id>/website', login_required(PropertyPlatformWebView.as_view()), name="psplatformweb"),
	path('settings/tracking-code/<str:uuid>', login_required(PropertyTrackingCodeView.as_view()), name="pstrackingcode"),
	path('settings/api-keys/<str:uuid>', login_required(PropertyAPIKeysView.as_view()), name="psapikeys"),
	path('settings/api-key-logs/<int:id>', login_required(PropertyAPIKeyLogsView.as_view()), name="psapikeylogs"),
	path('settings/do-not-track/<str:uuid>', login_required(PropertyDNTrackView.as_view()), name="psdntrack"),
	path('settings/do-not-track-ip/<str:uuid>', login_required(PropertyDNTrackIPView.as_view()), name="psdntrackip"),
	path('settings/do-not-track-email/<str:uuid>', login_required(PropertyDNTrackEmailView.as_view()), name="psdntrackemail"),
	path('settings/do-not-track-ip-delete/<int:id>', login_required(PropertyDNTrackIPDeleteView.as_view()), name="psdntrackipdelete"),
	path('settings/do-not-track-email-delete/<int:id>', login_required(PropertyDNTrackEmailDeleteView.as_view()), name="psdntrackemaildelete"),
	path('settings/webhooks/<str:uuid>', login_required(PropertyWebhooksView.as_view()), name="pswebhooks"),
	path('settings/customized-alerts/<str:uuid>', login_required(PropertyCAlertsView.as_view()), name="pscalerts"),

	path('uuid', login_required(PV.uuid), name="propertyUUID")
]