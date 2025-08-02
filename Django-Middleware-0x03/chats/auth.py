from rest_framework.exceptions import PermissionDenied

def ensure_user_in_conversation(user, conversation):
    if user not in conversation.participants.all():
        raise PermissionDenied("You do not belong to this conversation.")
