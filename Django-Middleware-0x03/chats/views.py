from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .pagination import MessagePagination
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant, IsParticipantOfConversation 
from rest_framework.exceptions import NotFound
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend



class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing conversation instances.
    """
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(participants=user).order_by('created_at')
        return Conversation.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Conversation deleted."}, status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing message instances.
    """
    queryset = Message.objects.all().order_by('sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        # Check if this is a nested route (conversations/{id}/messages/)
        conversation_id = self.kwargs.get("conversation_pk")  # From nested router
        
        if conversation_id:
            # This is the nested route: /conversations/{id}/messages/
            try:
                print(f"Fetching messages for conversation: {conversation_id}")
                conversation = Conversation.objects.get(pk=conversation_id)
            except Conversation.DoesNotExist:
                raise NotFound("Conversation not found.")
            
            print(f"Current user: {self.request.user}")
            print(f"Conversation participants: {list(conversation.participants.all())}")
            print(f"User in participants: {self.request.user in conversation.participants.all()}")

            # Check if user is a participant in the conversation
            if self.request.user not in conversation.participants.all():
                print(f"User not authorized for conversation: {conversation}")
                raise NotFound("You are not a participant in this conversation.")

            # Return all messages in the conversation
            messages_queryset = Message.objects.filter(conversation=conversation).order_by('sent_at')
            print(f"Number of messages found: {messages_queryset.count()}")
            return messages_queryset
        
        else:
            # This might be a direct message access or other route
            # Return empty queryset by default for security
            print("No conversation_pk found - returning empty queryset")
            return Message.objects.none()
    
    def create(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        conversation_id = request.data.get("conversation")
        print(f"Creating message in conversation: {conversation_id}")
        # conversation = Conversation.objects.get(pk=conversation_id)

        # if self.request.user not in conversation.participants.all():
        #     return Response(
        #         {"detail": "You are not allowed to send messages in this conversation."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Message deleted."}, status=status.HTTP_204_NO_CONTENT)
