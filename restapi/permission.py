from rest_framework.permissions import BasePermission


class GroupCheckPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='professor').exists() and request.method == 'GET':
            return True
        return False
