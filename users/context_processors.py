from .models import Profile,Message  # adjust this if your Message model is in another app


def has_unread_messages(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            has_unread = Message.objects.filter(receiver=profile, is_read=False).exists()
            return {'has_unread_messages': has_unread}
        except Profile.DoesNotExist:
            return {'has_unread_messages': False}
    return {}
