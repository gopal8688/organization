from django.urls import include, path
from django.contrib.auth.decorators import login_required
from api.views import HighRiskUsersView,DashboardStatsView,SecurityAlertsView,LoginAttemptsView,UserRiskAnalyticsView,RegionRiskDistView,RiskMapView,UsersListView,BasicUserDetailsView,LinkedUsersView,RecentUserActivitiesView,UserLocationsView

urlpatterns = [
	path('dashboard-stats/<int:id>/', login_required(DashboardStatsView.as_view()), name='ds'),
	path('high-risk-users/<int:id>/', login_required(HighRiskUsersView.as_view()), name='hru'),
	path('security-alerts/<int:id>/', login_required(SecurityAlertsView.as_view()), name='sa'),
	path('login-attempts/<int:id>/', login_required(LoginAttemptsView.as_view()), name='la'),
	path('user-risk-analytics/<int:id>/', login_required(UserRiskAnalyticsView.as_view()), name='ura'),
	path('region-risk-dist/<int:id>/', login_required(RegionRiskDistView.as_view()), name='rrd'),
	path('risk-map/<int:id>/', login_required(RiskMapView.as_view()), name='rm'),
	path('users-list/<int:id>/', login_required(UsersListView.as_view()), name='ul'),
	path('basic-user-details/<int:id>/', login_required(BasicUserDetailsView.as_view()), name='bud'),
	path('linked-users/<int:id>/', login_required(LinkedUsersView.as_view()), name='lus'),
	path('recent-user-activites/<int:id>/', login_required(RecentUserActivitiesView.as_view()), name='rua'),
	path('user-locations/<int:id>/', login_required(UserLocationsView.as_view()), name='ulo'),
]