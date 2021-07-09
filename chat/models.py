from django.db import models


class ChatRoomManager(models.Manager):

    def fetch_all_chat(self):
        return self.order_by('id').all()


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255)
    username = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )

    objects = ChatRoomManager()

    class Meta:
        db_table = "chatroom"


class ChatManager(models.Manager):

    def fetch_by_chat_id(self, chatroom_id):
        return self.filter(chatroom_id=chatroom_id).order_by('id')


class Chat(models.Model):
    chat = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    chatroom = models.ForeignKey(
        'ChatRoom', on_delete=models.CASCADE
    )

    objects = ChatManager()

    class Meta:
        db_table = "chat"
