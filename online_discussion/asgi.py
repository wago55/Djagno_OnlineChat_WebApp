# File Name		: asgi.py
# Version		: V1.0
# Designer		: 和合雅輝
# Date			: 2021.07.12
# Purpose      	: asgi設定

# Revision :
# V1.0 : 和合雅輝, 2021.07.12

"""
ASGI config for online_discussion project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# 環境変数を読ませる
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_discussion.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
import chat_channel.routing

# rouringに設定した、websocket_urlpatternsを走らせる
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(chat_channel.routing.websocket_urlpatterns)),
})
