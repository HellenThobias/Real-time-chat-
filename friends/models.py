from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE 
from django.utils import timezone

class FriendList(models.Model):
    user    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.username

    def add_friend(self, account):
        """
        Add new friends
        """

        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        remove friends
        """

        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        initiating a process of removing someone
        """
        remover_friends_list = self # a person termnating a friendship 

        # Remove friend from remover friends list: removee is the friend to be removed
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friendlist.
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    
    def is_mutual_friend(self, friend):
        """
        is this a friend?
        """
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """
    A friend request consist of two parties 
        1. Sender
            -Person sending or initiating a friend request
        2. Receiver
            -Person receiving a friend request
    """
    sender    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    
    def accept(self):
        """
        accept a friend request.
        update both SENDER an RECEIVER friendlists
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active=False
                self.save()

    def decline(self):
        """
        Decline a friend request.
        it is "declined" by setting the is_active' to False
        """
        self.is_active=False
        self.save()

    def cancel(self):
        """
        Cancel a friend request.
        it is "declined" by setting the is_active' to False
        It is different from declining a friends request on notifications that will be generated.
        """
        self.is_active=False
        self.save()