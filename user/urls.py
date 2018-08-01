from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login', views.UserView.as_view(), name='user_login'),
    re_path(r'user/(?P<pk>\d{1,5})/username',
            views.UpdateUsernameView.as_view(), name='update_username')
]
