from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from .views import DashboardView as DV#,HighRiskUsersView#, PropertySelection as PS

extra_patterns = [
	path('', login_required(DV.as_view()), name='home'),
	path('<int:id>/', login_required(DV.as_view()), name='pr-home'),
	#path('high-risk-users/<int:id>/', HighRiskUsersView.as_view(), name='hru'),
]

urlpatterns = [
	re_path('', include(extra_patterns))
]