from django.urls import include, path

from api.views import HighRiskUsersView,DashboardStatsView,SecurityAlertsView,LoginAttemptsView,UserRiskAnalyticsView,RegionRiskDistView,RiskMapView,UsersListView,BasicUserDetailsView,LinkedUsersView,RecentUserActivitiesView,UserLocationsView

urlpatterns = [
	path('dashboard-stats/<int:id>/', DashboardStatsView.as_view(), name='ds'),
	path('high-risk-users/<int:id>/', HighRiskUsersView.as_view(), name='hru'),
	path('security-alerts/<int:id>/', SecurityAlertsView.as_view(), name='sa'),
	path('login-attempts/<int:id>/', LoginAttemptsView.as_view(), name='la'),
	path('user-risk-analytics/<int:id>/', UserRiskAnalyticsView.as_view(), name='ura'),
	path('region-risk-dist/<int:id>/', RegionRiskDistView.as_view(), name='rrd'),
	path('risk-map/<int:id>/', RiskMapView.as_view(), name='rm'),
	path('users-list/<int:id>/', UsersListView.as_view(), name='ul'),
	path('basic-user-details/<int:id>/', BasicUserDetailsView.as_view(), name='bud'),
	path('linked-users/<int:id>/', LinkedUsersView.as_view(), name='lus'),
	path('recent-user-activites/<int:id>/', RecentUserActivitiesView.as_view(), name='rua'),
	path('user-locations/<int:id>/', UserLocationsView.as_view(), name='ulo'),
]