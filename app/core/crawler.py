from fake_useragent import UserAgent
from colorama import Fore, Style
import http.server
import socketserver
import threading
import time
import requests
import django
import json
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
                
        print(Fore.RED, "Processing job ...")
        jobName = target.targetName
        jobArg = target.targetUrl
        logType = f'{jobName}=>{jobArg}'
        LogModel.objects.create(logName='شروع خزیدن:', logType=logType,)
        headers = {'User-Agent': ua.random}
        print(Fore.BLUE,  f"START CRAWLING TO => {jobArg}")
        print(Fore.RED, f'{jobArg} SiteMap => {target.target_sitemap}' )
        sitemap_soup = crawler(f'https://{jobArg}/{target.target_sitemap}', headers=headers)
        LogModel.objects.create(logName='گزارش:', logType=f"{len(sitemap_soup)} عدد سایت مپ پیدا شد {jobName}")
        product_sitemap = get_products_sitemap(sitemap_soup)
        for i in product_sitemap:
            SiteMap.objects.create(target=jobArg, siteMapUrl=i)
            print(Fore.WHITE ,f'site map {i} saved to db')

        products_list = get_products_list(product_sitemap, ua)
        product_urls = []

        for i in products_list:
            if Product.objects.filter(product_url=i).exists():
                print(Fore.YELLOW, f'Product {i} is now exist!')
            else:
                Product.objects.create(product_url=i, product_parent=jobArg, product_type=target.targetType)
                print(Fore.BLUE, f'Product url: {i} saved to db')
            
        for z in range(len(products_list)):
            LogModel.objects.create(logName='گزارش:', logType=f"{len(product_urls)} عدد محصول پیدا شد {jobName}")
            product = requests.post('http://0.0.0.0:8080/api/get_products_url', {'jobArg': jobArg}).json()
            url = product['content'][0]['product_url']
            info = get_product_info(url, ua)
            if Product.objects.filter(product_parent=jobArg, product_url=url,  product_price=info['price']).exists():
                print(Fore.YELLOW ,f'NOT SAVE : Product {info}  in parent shop with prev price us exist! ')
            else:
                try:
                    res = requests.post('http://0.0.0.0:8080/api/store_products', {
                        'jobArg': jobArg,
                        'payload': json.dumps(info),
                        'url': i
                    }).json()
                    # Write Changes to csv
                    rows = []
                    stock_json = info['status']['quantity']
                    for variant in stock_json:
                        rows.append([
                            f'{jobArg}',
                            f"{info['name']} - {variant.get('color', 'N/A')}",
                            info['price'],
                            variant.get('quantity', 'N/A'),
                            i,
                        ])

                    filename = "Export_All.csv"

                    # Writing data to CSV file (append mode)
                    with open(filename, 'a', newline='') as file:
                        csvwriter = csv.writer(file)
                        csvwriter.writerows(rows)  # Append rows
                    
                    print(Fore.YELLOW, f'=> EXPORT UPDATED SUCCESSFULLY IN {filename}')
                    print(Style.RESET_ALL)

                except Exception as error:
                    print(Fore.RED ,f'Error: {error}')
                
        perform_comparison(jobArg)

        count = Product.objects.filter(product_parent=jobArg).count()
        
        logType = f"اتمام کار خزنده => سایت:{jobName} و تعداد {count} محصول اسکن شده"
        print(Fore.WHITE, f"\n\n{'^_^' * 5}\n\n{' ' * 4}=> CRAWLING IS FINISH ...")
        LogModel.objects.create(logName='پایان خزیدن', logType=logType)

def perform_comparison(jobArg):
    print(Fore.RED, f"\n =>  START PERFORM COMPARISON!  <=\n")
    response = requests.post('http://0.0.0.0:8080/api/perform_comparison', {}).json()
    LogModel.objects.create(logName='گزارش:', logType="مقایسه انجام شد")
    print(Fore.GREEN, f"\n --> COMPARISON  DONE !  <--\n")
    print(response)

def perform_crawl():
    ua = UserAgent()
    print(Fore.BLUE, "=> Perform the crawling job in an infinite loop.")
    while True:
        try:
            handle_job(ua)
            for i in range(SLEEP_DURATION):
                print(f'BOT SLEEP FOR {i} SEC')
                time.sleep(1)
            SiteMap.objects.all().delete()
        except Exception as e:
            print(e)
            log_error(str(e))

def start_server():
    print(Fore.RED, "Starting the HTTP server... ")
    with socketserver.TCPServer(("", SERVER_PORT), GetHandler) as httpd:
        print(Fore.YELLOW, f"Serving on port {SERVER_PORT}")
        httpd.serve_forever()

# Run the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Run the crawl function in the main thread
perform_crawl()