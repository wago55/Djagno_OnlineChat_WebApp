"""
ASGI config for online_discussion project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# import channels.asgi
# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application
# from channels.routing import URLRouter
# from channels.auth import AuthMiddlewareStack
# import chat_channel.routing
# from django.conf.urls import url


# import os
# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application
# from channels.routing import URLRouter, get_default_application
# from channels.auth import AuthMiddlewareStack
# import chat_channel.routing
# import django


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_discussion.settings')

# application = get_asgi_application()

# django_asgi_app = get_asgi_application()
#
# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': AuthMiddlewareStack(URLRouter(chat_channel.routing.websocket_urlpatterns)),
# })
#

# django_asgi_app = get_asgi_application()
#
# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': AuthMiddlewareStack(URLRouter(chat_channel.routing.websocket_urlpatterns)),
# })

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_discussion.settings')
# django.setup()
# django_asgi_app = get_asgi_application()
# application = get_default_application()

# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': AuthMiddlewareStack(URLRouter(chat_channel.routing.websocket_urlpatterns)),
# })

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

#application = get_asgi_application()
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter

from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
import chat_channel.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(chat_channel.routing.websocket_urlpatterns)),
})
