from email.policy import default
from django.db import models

from django.conf import settings
from django.utils import timezone

from account.models import Account

class FriendList(models.Model):
    user = models.OneToOneField('account.Account', on_delete=models.CASCADE, related_name = "user")
    friends = models.ManyToManyField(Account,blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self,account):
        "add friend"

        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)

    
    def unfrined(self,removee):
        # action of unfrining someone 
        remover_friends_list = self #person who terminate the friendshipp

        # remove friend from remover friend list 
        remover_friends_list.remove_friend(removee)

        # remove friend from removee friend list 
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)


    def is_mutual_friend(self,friend):
        # is this a friend 
        if friend in self.friends.all():
            return True
        return False



class FriendRequests(models.Model):
    '''
    friend request consists of two main parts
        Sender:
            - Person who send frnd req
        Receiver:
            - Person who receive frnd req

    '''

    sender = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('account.Account',on_delete=models.CASCADE, related_name="receiver")

    is_active = models.BooleanField(default=True,blank=True,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
            Accept Friend request
            Update both sender and receiver friends list
        """

        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)

            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active=True
                self.save()

    def decline(self):
        """
            Decline a friend request.
            it is declined by setting the is_active field to false.

        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request 
        It is canceled by setting the is active field to false.
        diff through the notification that generated. (sendr cancel his own send request)
        """
        self.is_active = False
        self.save()
        

