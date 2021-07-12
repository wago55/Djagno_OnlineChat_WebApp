# File Name		: wsgi.py
# Version		: V1.0
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: wsgi設定

# Revision :
# V1.0 : 和合雅輝, 2021.06.08


"""
WSGI config for online_discussion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# wsgi設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_discussion.settings')

application = get_wsgi_application()


