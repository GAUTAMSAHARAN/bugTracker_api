from rest_framework import permissions



class IsTeamMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        project = obj
        members = project.memebers.all()
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if user in list(members):
                return True
            else:
                return False

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        model = obj
        creater = model.creater
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if user.id == creater:
                return True
            else:
                return False


class IsUserBossOrNot(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.boss
