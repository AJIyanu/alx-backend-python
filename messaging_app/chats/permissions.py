from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

class IsParticipant(permissions.BasePermission):
    """
    Allows access only to participants of a conversation.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to the sender or conversation participant.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        conversation = getattr(obj, 'conversation', obj)

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if user in conversation.participants.all():
                return True
            raise PermissionDenied(detail="You are not allowed to modify this conversation.", code=status.HTTP_403_FORBIDDEN)

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return user in conversation.participants.all()

        return False