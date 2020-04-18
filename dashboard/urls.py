from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from .views import DashboardView as DV#, PropertySelection as PS

extra_patterns = [
	path('', login_required(DV.as_view()), name='home'),
	path('<int:id>/', login_required(DV.as_view()), name='pr-home')
]

urlpatterns = [
	re_path('', include(extra_patterns)),
	#path('<int:id>', PS.as_view(), name='prop_select'),
]