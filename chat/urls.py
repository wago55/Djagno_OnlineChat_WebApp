from django.urls import path
from . import views
from .views import ChatEnterRoomView, CreateChatRoomView, ChatroomDelete, ChatRoomUpdate
app_name = "chat"

urlpatterns = [
    path('chat_enter_room/', ChatEnterRoomView.as_view(), name="chat_enter"),
    path('chat_room_create/', CreateChatRoomView.as_view(), name="chat_room_create"),
    path('chat_room_delete/<int:pk>', ChatroomDelete.as_view(), name="chat_room_delete"),
    path('chat_room_update/<int:pk>', ChatRoomUpdate.as_view(), name="chat_room_update"),
    path('send_chat/<int:chatroom_id>', views.send_chat, name='send_chat'),
    path('save_chat/', views.save_chat, name='save_chat'),
]