Setup sec, local and stream.setup
____________________________________________________________________________
# PYTHON3 REQUIREMENTS
pip3 install pip3 install --upgrade pip && pip install django bs4 sockets requests aiohttp kavenegar fake-useragent aiogram openpyxl khayyam 
____________________________________________________________________________
# HOW USE DJANGO OUT SIDE DJANGO ?!
import django
import sys
import os

sys.path.append('/home/arashsorosh174/projects/python/shop_crawler/app/core')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
'core.settings'
django.setup()
from products.models import Product
____________________________________________________________________________
