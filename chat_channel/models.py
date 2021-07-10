# File Name		: models.py
# Version		: V1.1
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose       : チャット機能に関するデータモデルの設定

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.12 チャットルームのデータモデルを追加
# V1.2 : 平澤巧望, 2021.07.07 ChatRoomChannelの仕様抜けを修正


from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


class ChatRoomChannelManager(models.Manager):
    def create_room(self, room_name, chatroom_id, password=None):
        room = self.model(
            room_name=room_name,
            chatroom_id=chatroom_id,
            password=password
        )
        return room

#    def fetch_all_chat(self):
#        return self.order_by('id').all()


class ChatRoomChannel(models.Model):
    room_name = models.CharField(
        validators=[RegexValidator(r'^[a-zA-Z0-9]*$', 'You can input only alphabets or numbers.')],
        max_length=255
    )
    chatroom_id = models.CharField(
        validators=[MinLengthValidator(8), RegexValidator(r'^[0-9]*$', 'You can input only numbers(0-9).')],
        max_length=8, # chatroom_idは数字８桁で指定
        unique=True
    )
    username = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    password = models.CharField(
        validators=[MinLengthValidator(8)],
        max_length=19
    )
    is_active = models.BooleanField(default=True)

    objects = ChatRoomChannelManager()

    class Meta:
        db_table = "ChatRoomChannel"
    

class JoinChatRoom(models.Model):
    room_id = models.CharField(max_length=19)
    room_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150)

    def __str__(self):
        return '<Message:id' + str(self.id) + ',' + \
            self.room_name + '(' + self.username + ')>'
    
    class Meta: 
        ordering = ('room_name',)
