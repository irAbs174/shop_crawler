import http.server
import socketserver
import threading
import time

import django
import sys
import os

sys.path.append('/home/arashsorosh175/shop_crawler/app/core')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from func import *
from products.models import SiteMap, Product
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


def perform_crawl():
    while True:
        print("Performing scheduled crawler...")
        job = JobsModel.objects.first()
        jobName = job.jobName
        jobArg = job.jobArg
        if jobName == 'crawl':
            Product.objects.filter(product_parent=jobArg).delete()
            SiteMap.objects.all().delete()

            sitemap_soup = crawler(f'{jobArg}/sitemap_index.xml')
            product_sitemap = get_products_sitemap(sitemap_soup)
            for i in product_sitemap:
                SiteMap.objects.create(target=jobArg, siteMapUrl=i)
                print(f'site map {i} saved to db')
            
            products_list = get_products_list(product_sitemap)

            product_urls = []
            for i in products_list:
                Product.objects.create(product_url=i, product_parent=jobArg)
                product_urls.append(i)
                print(f'product url: {i} saved to db')

            for i in product_urls:
                info = get_product_info(i)
                Product.objects.all().filter(product_parent=jobArg, product_url=i).update(
                    product_name=info['name'],
                    product_price=info['price'],
                    product_stock=info['status'],
                )
                print(f'save product detail {info}')

            LogModel.objects.create(
                logName = f"{jobArg} => crawl-camplated",
                logType="notification",
                scanedProducts = f'{len(product.objects.filter(product_parent=jobArg))}',
            )

            JobsModel.objects.all().first().delete()

def comparison():
    our_product_name = input('enter our_product_name: \n')
    our_product_price = input('enter our_product_price: \n')
    main_dic = Product.objects.all()
    for i in main_dic:
        if i.product_name.find(our_product_name):
            print(f'product : {our_product_name} found !')
            if int(our_product_price) < int(i.product_price):
                print(f'PRODUCT DOWN !! => {our_product_name} < {i.product_name}')
                LogModel.objects.create(
                    logName="down",
                    logType= f'{our_product_name}<{i.product_name}',
                )
                Product.objects.filter(product_name=i.product_name).update(
                    product_status="down",
                )
            elif int(our_product_price) == int(i.price):
                print(f'equals price => {our_product_price} = {i.price}')
                Product.objects.filter(product_name=i.product_name).update(
                    product_status="equals",
                )
            else:
                print(f'{our_product_price} normal price')
                Product.objects.filter(product_name=i.product_name).update(
                    product_status="up",
                )
        else:
            print(f'product not exist! => {our_product_name} <=')

# Start the HTTP server
def start_server():
    with socketserver.TCPServer(("", 8080), GetHandler) as httpd:
        print(f"Serving on port 8080")
        perform_crawl()
        httpd.serve_forever()

start_server()