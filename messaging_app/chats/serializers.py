from rest_framework import serializers
from .models import User, Conversation, Message # Assuming your models are in users/models.py

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to include in the serialization.
        # It's generally good practice to explicitly list fields.
        # Do NOT include 'password' or 'password_hash' in `fields` or `exclude` here for security.
        # Django's AbstractUser handles password securely.
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'created_at',
            # 'username' # Include if you want to expose the username field from AbstractUser
        ]
        # Make fields read-only where necessary (e.g., auto-generated IDs, timestamps)
        read_only_fields = ['user_id', 'created_at']

        # Optional: You can add extra_kwargs for more control, e.g., to make a field write-only
        # extra_kwargs = {
        #     'password': {'write_only': True} # If you were handling password creation/change here
        # }


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    # To include the sender's email (or other identifying info) instead of just their ID
    sender_email = serializers.ReadOnlyField(source='sender.email')

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',          # This will be the sender's user_id (PK)
            'sender_email',    # The sender's email (read-only)
            'conversation',    # This will be the conversation's ID (PK)
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sender_email', 'sent_at']

        # If you want to make `sender` and `conversation` writeable by passing their IDs
        # and also include them in read-only representation:
        # extra_kwargs = {
        #     'sender': {'write_only': True},
        #     'conversation': {'write_only': True},
        # }


# --- Conversation Serializer (Nested) ---
class ConversationSerializer(serializers.ModelSerializer):
    # Nested field for participants:
    # Use UserSerializer to represent each participant fully.
    # many=True because there can be multiple participants.
    participants = UserSerializer(many=True, read_only=True)

    # Nested field for messages:
    # Use MessageSerializer to represent messages.
    # many=True because a conversation has multiple messages.
    # IMPORTANT: Ensure MessageSerializer does NOT nest ConversationSerializer back,
    # or you'll create an infinite recursion. We've avoided this by having
    # MessageSerializer only show `conversation` (ID) and not a nested object.
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',  # This will be the nested list of User objects
            'messages',      # This will be the nested list of Message objects
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

        # If you need to write participants when creating a conversation,
        # you would need a custom create/update method or use PrimaryKeyRelatedField
        # e.g., participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), write_only=True)