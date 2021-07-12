# File Name		: manage.py
# Version		: V1.0
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: manage.pyの設定 (Djangoのmigrateやrunserver等のコマンドを利用するためのスクリプト)

# Revision :
# V1.0 : 和合雅輝, 2021.06.08


#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_discussion.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
