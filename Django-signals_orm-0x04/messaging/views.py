from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def delete_user(request):
    """Allow a logged-in user to delete their account."""
    if request.method == "POST":
        user = request.user
        user.delete()  # Deletes the user and triggers the post_delete signal
        return redirect('home')  # Redirect after deletion (adjust 'home' as needed)
    return render(request, 'messaging/delete_user.html')


# View to display threaded conversations
def threaded_conversations(request):
    # Fetch all messages sent by the current user, including replies
    messages = Message.objects.filter(sender=request.user).select_related(
        'sender', 'receiver', 'parent_message'
    ).prefetch_related('replies')

    return render(request, 'messaging/threaded_conversations.html', {'messages': messages})


# Recursive function to fetch all replies to a specific message
def get_threaded_replies(message):
    replies = Message.objects.filter(parent_message=message).select_related(
        'sender', 'receiver', 'parent_message'
    ).prefetch_related('replies')

    threaded_replies = list(replies)
    for reply in replies:
        threaded_replies.extend(get_threaded_replies(reply))
    return threaded_replies


# View to fetch and display all replies to a specific message
def message_replies(request, message_id):
    # Get the parent message
    parent_message = get_object_or_404(Message, id=message_id, receiver=request.user)

    # Fetch threaded replies recursively
    all_replies = get_threaded_replies(parent_message)

    return render(request, 'messaging/message_replies.html', {
        'parent_message': parent_message,
        'replies': all_replies,
    })

def unread_messages(request):
    # Fetch unread messages for the current user using the custom manager
    unread_messages = Message.unread_messages.get_unread_messages(user=request.user)

    return render(request, 'messaging/unread_messages.html', {'unread_messages': unread_messages})
