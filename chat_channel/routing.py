# File Name		: routing.py
# Version		: V1.0
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: チャット機能に関するroutingの設定

# Revision :
# V1.0 : 和合雅輝, 2021.06.08

from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]
