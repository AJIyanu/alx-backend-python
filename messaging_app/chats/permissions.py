from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Allows access only to participants of a conversation.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Allows access only to the sender or conversation participant.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.sender == user or
            user in obj.conversation.participants.all()
        )
