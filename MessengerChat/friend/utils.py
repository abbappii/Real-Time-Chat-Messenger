from friend.models import FriendRequests

def get_friend_request_or_false(sender,receiver):
    try:
        return FriendRequests.objects.get(sender=sender,receiver=receiver,is_active=True)
    except FriendRequests.DoesNotExist:
        return False
        