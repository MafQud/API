from django.utils import timezone
from rest_framework import permissions


class IsVerified(permissions.BasePermission):
    """
    Checks whether a user has verified his identity
    """

    # Override the default detail message of PermissionDenied
    message = "User has not verified his identity yet"

    def has_permission(self, request, view):
        id_exp = request.user.id_exp_date
        return id_exp is not None and id_exp > timezone.now()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Checks whether a user is the creator of a certain
    object, otherwise read only access is allowed
    """

    # Call this inside views ⬇️
    # check_object_permissions(request, obj)

    message = "User doesn't have the previlages"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.user
