import django
import sys
import os

sys.path.append('/home/arashsorosh174/projects/python/shop_crawler/app/core')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
'core.settings'
django.setup()