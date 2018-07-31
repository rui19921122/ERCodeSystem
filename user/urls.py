from django.urls import path
from . import views

urlpatterns = [
    path('login', views.UserView.as_view(), name='user_login')
]
