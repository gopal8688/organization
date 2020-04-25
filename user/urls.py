from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from .views import UserView,UserDetailView

urlpatterns = [
	path('<int:pid>/', login_required(UserView.as_view()), name="userindex"),
	path('<int:pid>/<str:username>/', login_required(UserDetailView.as_view()), name="userdetail")
]

# extra_patterns = [
# 	path('<int:id>/', DV.as_view(), name='userindex')
# ]

# urlpatterns = [
# 	re_path('', include(extra_patterns))
# ]