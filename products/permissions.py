from rest_framework.permissions import BasePermission


class ProductPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous and view.action in \
                ['list', 'retrieve']:
            return True
        if view.action in ['create', 'partial_update', 'destroy'] and \
                request.user.is_authenticated and request.user.is_superuser \
                and request.user.is_active:
            return True
        else:
            return False


class ProductImagePermission(BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create'] and \
                request.user.is_authenticated and request.user.is_superuser \
                and request.user.is_active:
            return True
        else:
            return False
