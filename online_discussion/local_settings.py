# File Name		: local_settings.py
# Version		: V1.0
# Designer		: 和合雅輝
# Date			: 2021.07.12
# Purpose      	: asgi設定

# Revision :
# V1.0 : 和合雅輝, 2021.07.12


import os
from pathlib import Path

# ローカルでの設定
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^7afl9)n+g9m5hg6zwczn1w7-wzd_$l-a6mhc7#19yd@g2)oz#'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = False #ローカルでDebugできるようになります