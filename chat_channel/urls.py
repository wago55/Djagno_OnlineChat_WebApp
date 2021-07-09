# File Name		: urls.py
# Version       : V1.1
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: 

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.12 チャットルーム認証機能に対応
# V1.2 : 高橋龍平, 2021.06.18 カウントダウン機能に対応

from django.urls import path
from .import views
from .views import Chat, LoginChatRoomView, ChatRoomLeaveView, TimerView
from .views import CreateChatRoomView, CreateChatRoomSuccessView, CreateChatRoomFailedView, LoginChatRoomFailedView

app_name= 'chat_channel'

urlpatterns = [
#    path('chat/', views.chat, name="chat"),
    path('chat/', Chat.as_view(), name="chat"),
    path('chat_room_login/', LoginChatRoomView.as_view(), name="chat_room_login"),
    path('chat_room_login_Failed/', LoginChatRoomFailedView.as_view(), name="login_failed"),
    path('chat_room_create/', CreateChatRoomView.as_view(), name="chat_room_create"),
    path('chat_room_create_success/', CreateChatRoomSuccessView.as_view(), name="create_success"),
    path('chat_room_create_Failed/', CreateChatRoomFailedView.as_view(), name="create_failed"),
    path('chat_room_leave/', ChatRoomLeaveView.as_view(), name="leave"),
    path('chat_room_detail/<room_id>', views.room_detail, name="chat_room_detail"),
    path('delete_joinchatroom/<int:num>', views.delete_joinchatroom, name="delete_joinchatroom"),
    path('timer/', TimerView.as_view(), name='timer'),

]
