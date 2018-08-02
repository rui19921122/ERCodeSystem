from django.contrib.auth.models import User, AnonymousUser
from rest_framework.permissions import BasePermission


class UserCanSetUserInfo(BasePermission):
    """
    用户是否可以更改其他人的信息
    """

    def has_permission(self, request, view):
        return request.user.has_perm('user.can_set_username') \
               or request.user.is_superuser
