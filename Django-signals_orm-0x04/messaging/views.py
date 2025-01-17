from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    """Allow a logged-in user to delete their account."""
    if request.method == "POST":
        user = request.user
        user.delete()  # Deletes the user and triggers the post_delete signal
        return redirect('home')  # Redirect after deletion (adjust 'home' as needed)
    return render(request, 'messaging/delete_user.html')
