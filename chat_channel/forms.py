# File Name		: forms.py
# Version	    : V1.1
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose       : チャットルームの登録・認証のためのフォームの定義

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.12 チャットルーム認証機能に対応


from django import forms
from .models import ChatRoomChannel, JoinChatRoom

class CreateChatRoomForm(forms.ModelForm):
    room_name = forms.CharField(label='ルーム名')
    chatroom_id = forms.CharField(label='ルームID')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = ChatRoomChannel
        fields = ('room_name', 'chatroom_id', 'password')


class LoginChatRoomForm(forms.Form):
    chatroom_id = forms.CharField(label='ルームID')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

class JoinChatRoomForm(forms.ModelForm):
    class Meta:
        model = JoinChatRoom
        fields = ['room_name','username']
