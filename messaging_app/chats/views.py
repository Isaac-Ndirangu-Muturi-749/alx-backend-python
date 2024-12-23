from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404


# ViewSet for Conversations
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=False, methods=['post'], url_path='create', url_name='create_conversation')
    def create_conversation(self, request):
        """
        Endpoint to create a new conversation.
        Expects a list of participant user IDs in the request data.
        """
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


# ViewSet for Messages
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Endpoint to send a message to an existing conversation.
        Expects conversation_id and message_body in the request data.
        """
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')
        sender = request.user  # Assumes authentication and request.user is the sender

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, pk=conversation_id)
        message = Message.objects.create(conversation=conversation, sender=sender, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
