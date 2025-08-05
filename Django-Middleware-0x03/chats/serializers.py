from rest_framework import serializers
from .models import User, Conversation, Message

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'role',
            'created_at',
        ]
        read_only_fields = ['user_id', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_role(self, value):
        allowed_roles = ['guest', 'host', 'admin']
        if value not in allowed_roles:
            raise serializers.ValidationError("Invalid role specified.")
        return value


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

 


class ConversationSerializer(serializers.ModelSerializer):
 
    # participants = UserSerializer(many=True, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all()
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages', 
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']
