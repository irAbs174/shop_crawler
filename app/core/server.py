import socket
import threading
import time
import django
import sys
import os
import time

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
            jobName = JobsModel.objects.all().first().jobName
            jobArg = JobsModel.objects.all().first().jobArg
            
            if jobName == 'crawl':
                client_socket.send(f"target=>{jobArg}".encode('utf-8'))
                message = client_socket.recv(1024).decode('utf-8')

                while 'sitemap_url=>' in message:
                    sitemap = message.decode('utf-8').split('=>')[1]
                    SiteMap.objects.create(
                        target=jobArg,
                        siteMapUrl=sitemap,
                    )
                    print(f'site map {sitemap} saved to db')
                
                while 'give_me_sitemap_to_crawl' in message:
                    for i in SiteMap.objects.all().filter(target=jobArg):
                        client_socket.send(f'sitemap_to_crawl=>{i.siteMapUrl}'.encode('utf-8'))
                        time.sleep(5)

                while 'product_url=>' in message:
                    url = message.decode('utf-8').split('=>')[1]
                    Product.objects.create(
                        product_url=url,
                        product_parent=jobArg,
                    )
                    client_socket.send(f'get_product_info=>{url}'.encode('utf-8'))

                while 'give_me_product_url' in message:
                    url = Product.objects.filter(product_parent=jobArg, product_price='').first().product_url
                    client_socket.send(url.encode('utf-8'))

                while 'product_info=>' in message:
                    msg = message.decode('utf-8').split('=>')
                    product_name = msg[1]
                    product_price = msg[2]
                    product_stock = msg[3]
                    product_url = msg[4]
                    Products.objects.all().filter(product_url=product_url).update(
                        product_name = product_name,
                        product_price = product_price,
                        product_stock = product_stock,
                    )
                    
                else:
                    print('lissing ...')
        except:
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