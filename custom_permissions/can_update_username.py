from django.contrib.auth.models import User,AnonymousUser
from rest_framework.permissions import BasePermission


class UserCanUpdateUsername(BasePermission):
    def has_permission(self, request, view):
        assert isinstance(request.user, User or AnonymousUser)
        return request.user.has_perm('user.can_set_username')