import socket
import threading
import time
from functions import *

def send_message(server_socket):
    while True:
        response = server_socket.recv(1024).decode('utf-8')
        print(f"SERVER_MSG => {response}")
        while 'target=>' in response:
            target = response.split('=>')[1]
            print(f'Start crawling to {target}')
            sitemap_soup = crawler(f'{target}/sitemap_index.xml')
            products_sitemap = get_products_sitemap(sitemap_soup)
            for i in products_sitemap:
                server_socket.send(f"sitemap_url=>{i}".encode('utf-8'))
                time.sleep(1.5)

            server_socket.send("give_me_sitemap_to_crawl".encode('utf-8'))
            
        while 'sitemap_to_crawl=>' in response:
            sitemap = response.split('=>')[1]
            product_list = get_products_list(sitemap)
            for i in product_list:
                server_socket.send(f"product_url=>{i}".encode('utf-8'))
                time.sleep(1.5)

        while 'get_product_info=>' in message:
            product_url = message.split('=>')[1]
            info = get_product_info(product_url)
            name = info['name']
            price = info['price']
            stock = info['status']
            server_socket.send(f"product_info=>{name}=>{price}=>{stock}=>{product_url}")
        else:
            rint('waiting ...')
        time.sleep(5)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('127.0.0.1', 8778))
    print("Connected to the server.")
    
    message_sender = threading.Thread(target=send_message, args=(server,))
    message_sender.start()

if __name__ == "__main__":
    start_server()
