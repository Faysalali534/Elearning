from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='professor').exists():
            return True
        elif request.method == 'GET':
            return True
        return False
