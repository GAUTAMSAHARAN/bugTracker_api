from rest_framework import permissions


class ProjectOwner(permissions.BasePermission):

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

class IssueOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        issue = obj
        creater = issue.creater
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if user.id == creater:
                return True
            else:
                return False

class CommentOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        comment = obj
        creater = comment.creater
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
