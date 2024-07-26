import http.server
import socketserver
import threading
import time

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

from fake_useragent import UserAgent

# Import models and functions
from func import *
from products.models import SiteMap, Product, UsProduct
from target.models import TargetModel
from jobs.models import JobsModel
from logs.models import LogModel

class GetHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, world!")
        return

def log_error(message):
    """Log errors to the database."""
    LogModel.objects.create(logName='error', logType="error", errorMessage=message)

def handle_job(job, ua):
    """Process a single job."""
    jobName = job.jobName
    jobArg = job.jobArg
    headers = {'User-Agent': ua.random}
    if jobName == 'crawl':
        Product.objects.filter(product_parent=jobArg).delete()
        SiteMap.objects.all().delete()

        sitemap_soup = crawler(f'{jobArg}/sitemap_index.xml', headers=headers)
        product_sitemap = get_products_sitemap(sitemap_soup)
        for i in product_sitemap:
            SiteMap.objects.create(target=jobArg, siteMapUrl=i)
            print(f'site map {i} saved to db')

        products_list = get_products_list(product_sitemap, ua)

        product_urls = []
        for i in products_list:
            Product.objects.create(product_url=i, product_parent=jobArg)
            product_urls.append(i)
            print(f'product url: {i} saved to db')

        for i in product_urls:
            info = get_product_info(i, ua)
            Product.objects.filter(product_parent=jobArg, product_url=i).update(
                product_name=info['name'],
                product_price=info['price'],
                product_stock=info['status'],
            )
            print(f'save product detail {info}')

        LogModel.objects.create(
            logName=f"{jobArg} => crawl-completed",
            logType="notification",
            scanedProducts=f'{len(Product.objects.filter(product_parent=jobArg))}',
        )

        perform_comparison()
        
        job.delete()
        LogModel.objects.filter(logName='bot_status').update(logType="offline")

def perform_comparison():
    """Compare product prices between main and US products."""
    us_dic = UsProduct.objects.all()
    main_dic = Product.objects.all()
    for main_product, us_product in zip(main_dic, us_dic):
        if main_product.product_name.find(us_product.us_product_name) != -1:
            print(f'product : {us_product.us_product_name} found !')
            if int(us_product.us_product_price) < int(main_product.product_price):
                print(f'PRODUCT DOWN !! => {us_product.us_product_name} < {main_product.product_name}')
                LogModel.objects.create(
                    logName="down",
                    logType=f'{us_product.us_product_name}<{main_product.product_name}',
                )
                Product.objects.filter(product_name=main_product.product_name).update(
                    product_status="down",
                )
            elif int(us_product.us_product_price) == int(main_product.product_price):
                print(f'equals price => {us_product.us_product_price} = {main_product.product_price}')
                Product.objects.filter(product_name=main_product.product_name).update(
                    product_status="equals",
                )
            else:
                print(f'{us_product.us_product_name} normal price')
                Product.objects.filter(product_name=main_product.product_name).update(
                    product_status="up",
                )
        else:
            print(f'product not exist! => {us_product.us_product_name} <=')

def perform_crawl():
    ua = UserAgent()

    """Perform the crawling job in an infinite loop."""
    while True:
        try:
            LogModel.objects.create(logName='bot_status', logType="online")
            job = JobsModel.objects.first()
            if job:
                handle_job(job, ua)
            time.sleep(SLEEP_DURATION)
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
