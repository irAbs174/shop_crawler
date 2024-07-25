import socket
import threading
import time
import django
import sys
import os

sys.path.append('/home/arashsorosh175/shop_crawler/app/core')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from products.models import SiteMap, Product
from target.models import TargetModel
from jobs.models import JobsModel
from logs.models import LogModel

def handle_client(client_socket):
    while True:
        try:
            job = JobsModel.objects.first()
            jobName = job.jobName
            jobArg = job.jobArg
            
            if jobName == 'crawl':
                client_socket.send(f"target=>{jobArg}".encode('utf-8'))
                message = client_socket.recv(1024).decode('utf-8')

                if 'sitemap_url=>' in message:
                    sitemap = message.split('=>')[1]
                    SiteMap.objects.create(target=jobArg, siteMapUrl=sitemap)
                    print(f'site map {sitemap} saved to db')
                
                if 'give_me_sitemap_to_crawl' in message:
                    for i in SiteMap.objects.filter(target=jobArg):
                        client_socket.send(f'sitemap_to_crawl=>{i.siteMapUrl}'.encode('utf-8'))
                        time.sleep(5)

                if 'product_url=>' in message:
                    url = message.split('=>')[1]
                    Product.objects.create(product_url=url, product_parent=jobArg)
                    client_socket.send(f'get_product_info=>{url}'.encode('utf-8'))

                if 'give_me_product_url' in message:
                    product = Product.objects.filter(product_parent=jobArg, product_price='').first()
                    if product:
                        client_socket.send(f"product_url=>{product.product_url}".encode('utf-8'))

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
