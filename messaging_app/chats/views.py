from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing conversation instances.
    """
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_conversations = Conversation.objects.filter(participants=user)
            return Message.objects.filter(conversation__in=user_conversations).order_by('sent_at')
        return Message.objects.none()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Message deleted."}, status=status.HTTP_204_NO_CONTENT)
    
    # filters
