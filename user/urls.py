from django.urls import include, path, re_path

from .views import UserView,UserDetailView

urlpatterns = [
	path('<int:pid>/', UserView.as_view(), name="userindex"),
	path('<int:pid>/<str:username>/', UserDetailView.as_view(), name="userdetail")
]

# extra_patterns = [
# 	path('<int:id>/', DV.as_view(), name='userindex')
# ]

# urlpatterns = [
# 	re_path('', include(extra_patterns))
# ]