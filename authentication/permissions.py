from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_active and \
                not request.user.is_superuser and view.action in \
                ['partial_update', 'destroy', 'change_password', 'me']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not obj == request.user:
            return False
        else:
            return True


class LoginSignupPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        else:
            return False
