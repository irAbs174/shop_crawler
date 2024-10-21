#!/bin/bash

#GRAND ACCRESS TO THIS FILE WITH EXECUTE:
#chmod 755 deploy.sh

#EXECUTE THIS FILE TO INSTALL PROJECT REQUIREMENTS
clear
echo "SHOP CRAWLER V0.0.1 BY 174"

#sudo apt install python3 python3-venv
#python3 -m venv env
#source env/bin/activate
#pip3 install --upgrade pip && pip install django django-cors-headers bs4 sockets requests aiohttp kavenegar fake-useragent aiogram openpyxl khayyam colorama selenium webdriver_manager

python3 app/core/crawler.py


