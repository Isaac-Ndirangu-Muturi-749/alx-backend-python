from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)  # Timestamp of the last edit
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name="edited_messages", on_delete=models.SET_NULL)  # User who edited the message

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} at {self.timestamp}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id} at {self.timestamp}"
