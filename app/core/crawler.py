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
                Product.objects.all().filter(product_parent=jobArg).update(
                    product_name=info['name'],
                    product_price=info['price'],
                    product_stock=info['status'],
                    product_url=jobArg,
                )
                print(f'save product detail {info}')

        # Add your job logic here
        time.sleep(3 * 60 * 60)  # Sleep for 3 hours

# Start the HTTP server
def start_server():
    with socketserver.TCPServer(("", 8080), GetHandler) as httpd:
        print(f"Serving on port 8080")
        perform_crawl()
        httpd.serve_forever()

start_server()

'''
def handle_client(client_socket):
    while True:
        try:

                client_socket.send(f"target=>{jobArg}".encode('utf-8'))
                message = client_socket.recv(1024).decode('utf-8')

                if 'sitemap_url=>' in message:

                
                if 'give_me_sitemap_to_crawl' in message:
                    for i in SiteMap.objects.filter(target=jobArg):
                        client_socket.send(f'sitemap_to_crawl=>{i.siteMapUrl}'.encode('utf-8'))
                        time.sleep(5)

                if 'product_url=>' in message:
                    url = message.split('=>')[1]
                    
                    client_socket.send(f'get_product_info=>{url}'.encode('utf-8'))

                if 'give_me_product_url' in message:

                if 'product_info=>' in message:
                    msg = message.split('=>')
                    product_name = msg[1]
                    product_price = msg[2]
                    product_stock = msg[3]
                    product_url = msg[4]
                    Product.objects.filter(product_url=product_url).update(
                        product_name=product_name,
                        product_price=product_price,
                        product_stock=product_stock
                    )
                else:
                    print('listening ...')
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind(('0.0.0.0', 8778))
    client.listen(5)
    print("SERVER started, waiting for connections...")
    
    while True:
        client_socket, addr = client.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_client()

'''