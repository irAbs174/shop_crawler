import http.server
import socketserver
import threading
import time
from fake_useragent import UserAgent
import requests
import django
import sys
import csv
import os

# Constants
SYS_PATH = '/home/arashsorosh175/shop_crawler/app/core'
DJANGO_SETTINGS_MODULE = "core.settings"
SERVER_PORT = 8090
SLEEP_DURATION = 10  # 240 minutes

# Django setup
sys.path.append(SYS_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
django.setup()

# Import models and functions
from django.utils import timezone

from func import *
from products.models import SiteMap, Product, UsProduct
from target.models import TargetModel
from jobs.models import JobsModel
from logs.models import LogModel

today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

class GetHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"GET OUT HERE !!")
        return

def log_error(message):
    """Log errors to the database."""
    LogModel.objects.create(logName='error', logType="error")

def handle_job(ua):
    targets = TargetModel.objects.all()
    for target in targets:
                
        """Process a single job."""
        jobName = target.targetName
        jobArg = target.targetUrl
        headers = {'User-Agent': ua.random}
        print("start")
        print(jobArg,target.target_sitemap )
        sitemap_soup = crawler(f'https://{jobArg}/{target.target_sitemap}', headers=headers)
        product_sitemap = get_products_sitemap(sitemap_soup)
        for i in product_sitemap:
            SiteMap.objects.create(target=jobArg, siteMapUrl=i)
            print(f'site map {i} saved to db')

        products_list = get_products_list(product_sitemap, ua)

        product_urls = []

        for i in products_list:
            if Product.objects.filter(product_url=i, product_parent=jobArg).exists():
                product_urls.append(i)
                print(f'=>{i} Exist!')
            else:
                Product.objects.create(product_url=i, product_parent=jobArg, product_type=target.targetType)
                product_urls.append(i)
                print(f'product url: {i} saved to db')

        if product_urls:
            for i in product_urls:  
                info = get_product_info(i, ua)
                if Product.objects.filter(product_url=i, product_parent=jobArg,  product_price=info['price']).exists():
                    print(f'=>{i} Exist!')
                else:
                    Product.objects.filter(product_parent=jobArg, product_url=i).update(
                        product_name=info['name'],
                        product_price=info['price'],
                        product_stock=info['status'],
                    )
                    print(f'save product detail {info}')
        else:
            print("Not Url")

        LogModel.objects.create(
            logName=f"{jobArg} => crawl-completed",
            logType="notification",
            scanedProducts=f'{len(Product.objects.filter(product_parent=jobArg))}',
        )

        perform_comparison(jobArg)

        perform_export(jobName, jobArg)
        
        LogModel.objects.filter(logName='bot_status').update(logType="offline")

def perform_comparison(jobArg):
    ctx = {
        'jobArg': jobArg,
    }
    response = requests.post('http://0.0.0.0:8080/api/perform_comparison', ctx).json()
    print(response)

def perform_export(jobName, jobArg):
    fields = ['فروشگاه', 'نام محصول', 'قیمت', 'وضعیت', 'موجودی', 'آدرس محصول']
    rows = []
    response = requests.post('http://0.0.0.0:8080/api/get_products_api', data={})
    for i in response.json()['status']:
        if i['price'] == '0':
            stock = 'ناموجود'
        elif i['stock'] == 'ناموجود':
            stock = 'ناموجود'
        else:
            stock = 'موجود'
        rows.append([
            i['parent'],
            i['name'],
            i['price'],
            i['status'],
            stock,
            i['url'],
        ])
    # name of csv file
    filename = f"Products_Export=>{jobName}.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)

    print(f'EXPORT => {jobArg}')

def perform_crawl():
    ua = UserAgent()
    """Perform the crawling job in an infinite loop."""
    while True:
        try:
            LogModel.objects.create(logName='bot_status', logType="online")
            handle_job(ua)
            for i in range(SLEEP_DURATION):
                print(f'BOT SLEEP FOR {i} SEC')
                time.sleep(1)
            SiteMap.objects.all().delete()
        except Exception as e:
            print(e)
            log_error(str(e))

def start_server():
    """Start the HTTP server."""
    with socketserver.TCPServer(("", SERVER_PORT), GetHandler) as httpd:
        print(f"Serving on port {SERVER_PORT}")
        httpd.serve_forever()

# Run the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Run the crawl function in the main thread
perform_crawl()
