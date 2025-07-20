from rest_framework import serializers
from .models import User, Conversation, Message # Assuming your models are in users/models.py

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'created_at',
        ]
        read_only_fields = ['user_id', 'created_at']


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source='sender.email')

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_email',    
            'conversation',    
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sender_email', 'sent_at']

 


# --- Conversation Serializer (Nested) ---
class ConversationSerializer(serializers.ModelSerializer):
 
    participants = UserSerializer(many=True, read_only=True)

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
