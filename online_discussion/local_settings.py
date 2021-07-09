import os
from pathlib import Path

#settings.pyからそのままコピー
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^7afl9)n+g9m5hg6zwczn1w7-wzd_$l-a6mhc7#19yd@g2)oz#'

#settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = False #ローカルでDebugできるようになります