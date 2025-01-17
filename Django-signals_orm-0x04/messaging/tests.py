from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification
from django.utils.timezone import now

class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')
        self.message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Original Message")

    def test_message_edit_logs_history(self):
        # Edit the message
        self.message.content = "Edited Message"
        self.message.save()

        # Check if the edit was logged in MessageHistory
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original Message")

        # Check if edited fields are updated
        self.assertTrue(self.message.edited)
        self.assertIsNotNone(self.message.edited_at)
        self.assertEqual(self.message.edited_by, self.sender)

    def test_notification_created_on_message(self):
        # Create a message
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")

        # Check if a notification is created
        notification = Notification.objects.filter(user=self.receiver, message=message)
        self.assertTrue(notification.exists())
