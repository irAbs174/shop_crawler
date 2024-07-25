import sys
import django
import os

sys.path.append('/home/arashsorosh175/shop_crawler/app/core')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()