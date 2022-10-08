from enum import unique
from tokenize import blank_re
from django.db import models
from psycopg2 import Timestamp

# Create your models here.
class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField('account.Account',help_text="users who are connected to this chat room.",blank=True)

    def __str__(self):
        return self.title

    def connect_user(self,user):
        """
            return true if user is added to users list
        """

        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.sava()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self,user):
        """
            return true if user removed from the users group list.
        """

        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed
    
    @property
    def group_name(self):
        """
		Returns the Channels Group name that sockets should subscribe to to get sent
		messages as they are generated.
		"""
        return "PublicChatRoom-%s" % self.id


class PublicRoomMessageManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomMessage.objects.filter(room=room).order_by('-timestamp')
        return qs

class PublicRoomMessage(models.Model):
    """
        Chat message created by a user from public chat room.
    """

    user = models.ForeignKey('account.Account',on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom,on_delete=models.CASCADE)
    content =  models.TextField(unique=False,blank=False)

    timestamp = models.DateTimeField(auto_now_add = True)

    objects = PublicRoomMessageManager()

    def __str__(self):
        return self.content