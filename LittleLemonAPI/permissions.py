from rest_framework.permissions import BasePermission


class isManager(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Manager'):
            return True
        return False

class isCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.user and not request.user.groups.filter(name='Manager') and not request.user.groups.filter(name='delivery_crew') :
            return True
        return False
    
class isdeliverycrew(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='delivery_crew') :
            return True
        return False