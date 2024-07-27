import django
import sys
import os

# Constants
SYS_PATH = '/home/arashsorosh175/shop_crawler/app/core'
DJANGO_SETTINGS_MODULE = "core.settings"
SERVER_PORT = 8080
SLEEP_DURATION = 3600  # 60 minutes

# Django setup
sys.path.append(SYS_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
django.setup()