from django.db import models
from account.models import Account



class PublicChatRoom(models.Model):
    title = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(Account, blank=True, help_text="number of users who are connected to the chat")

    def __str__(self):
        return self.title

    def connect_user(self, user):
        is_connected = False
        # check if user is connected

        if user not in self.users.all():
            self.users.add(user)
            self.save()
            is_connected = True
        
        elif user in self.users.all():
            is_connected = True

        return is_connected

    def disconnect_user(self, user):
        is_disconnected = False
        # check if user is connected

        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_disconnected = True

        return is_disconnected

    @property
    def group_name(self):
        return f"PublicChatRoom-{self.id}"


class PublicChatMessageManager(models.Manager):
     def by_room(self, room):
         qs = PublicChatMessage.objects.filter(room=room).order_by("-timestamp")
         return qs


class PublicChatMessage(models.Model):
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PublicChatMessageManager()

    def __str__(self):
        return self.content

    
    