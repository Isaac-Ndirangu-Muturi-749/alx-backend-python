from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    permission_classes = [IsAuthenticated, IsOwner]  # Ensure only the owner can access their conversation

    @action(detail=False, methods=['post'], url_path='create', url_name='create_conversation')
    def create_conversation(self, request):
        participants = request.data.get('participants', [])
        if not participants:
            return Response(
                {"error": "Participants list cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
            serializer = self.get_serializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__email']
    permission_classes = [IsAuthenticated, IsOwner]  # Ensure only the owner can access their messages

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')
        sender = request.user

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, pk=conversation_id)
        message = Message.objects.create(conversation=conversation, sender=sender, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user)
