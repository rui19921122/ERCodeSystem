"""ERCodeSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title=f"{settings.PROJECT_NAME} 的API文档",
        default_version='v1',
        description=f"{settings.PROJECT_NAME} 的API文档，使用redoc进行构建",
        contact=openapi.Contact(email="501312506@qq.com",name='han'),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # api文档相关配置
    re_path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path('admin/', admin.site.urls),
    # 用户信息配置
    path('user/', include('user.urls')),
]
