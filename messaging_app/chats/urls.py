from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Define app-specific URLs
urlpatterns = [
    path('', include(router.urls)),
]