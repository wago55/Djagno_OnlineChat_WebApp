from django import forms
from .models import ChatRoom, Chat


class CreateChatRoomForm(forms.ModelForm):
    room_name = forms.CharField(label='チャットルーム名')

    class Meta:
        model = ChatRoom
        fields = ('room_name',)


class DeleteChatRoomForm(forms.ModelForm):

    class Meta:
        model = ChatRoom
        fields = ()


class SendChatForm(forms.ModelForm):
    chat = forms.CharField(label="", widget=forms.Textarea(attrs={'row': 5, 'cols': 60}))

    class Meta:
        model = Chat
        fields = ('chat',)


