# File Name		: admin.py
# Version		: V1.0
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: 管理サイトの設定

# Revision :
# V1.0 : 和合雅輝, 2021.06.08

from django.contrib import admin
from .models import ChatRoomChannel, JoinChatRoom

# 管理サイトに表示するモデルの設定
admin.site.register(ChatRoomChannel)
admin.site.register(JoinChatRoom)


