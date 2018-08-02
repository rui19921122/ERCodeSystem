from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login', views.UserView.as_view(), name='user_login'),
    re_path(r'(?P<pk>\d{1,5})/',
            views.UpdateUsernameAndPermissionView.as_view(),
            name='update username and permission'),
    path('list/', views.QueryAllUserInfoView.as_view(), name='query_users')
]
