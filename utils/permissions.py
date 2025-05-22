from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    """
    Custom permission to only allow staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsOwnerOrStaff(BasePermission):
    """
    Custom permission to only allow owners of an object or staff to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Staff can access any object
        if request.user.is_staff:
            return True
        
        # Check if object has an owner field
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        return False
