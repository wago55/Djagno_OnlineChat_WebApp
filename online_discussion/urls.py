# File Name		: urls.py
# Version		: V1.0
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: 各アプリのurls.pyを読み込ませる.

# Revision :
# V1.0 : 和合雅輝, 2021.06.08


from django.contrib import admin
from django.urls import path, include

# 各アプリのurls.pyを読ませる
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('chat_channel/', include('chat_channel.urls')),
]
