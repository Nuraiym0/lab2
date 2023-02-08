from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Course

class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if isinstance(obj, Course):
            return request.user == obj.course.author
        return request.user == obj.author


class IsMentor(BasePermission):
    def has_object_permission(self, request, view, obj):
       return request.user.is_mentor 
