from tools.functions import *


def handle_crawler():
    address = input('Enter valid address (HTTP/HTTPS is required): ')
    if address.startswith('https://') or address.startswith('http://'):
        print(crawler(address))
    else:
        print("Invalid address. Must start with HTTP/HTTPS.")

def handle_products_sitemap():
    address = input('Enter valid sitemap.xml or sitemap_index.xml (HTTP/HTTPS is required): ')
    if address.startswith('https://') or address.startswith('http://'):
        sitemap_soup = crawler(address)
        if sitemap_soup:
            print(get_products_sitemap(sitemap_soup))
    else:
        print("Invalid address. Must start with HTTP/HTTPS.")

def handle_products_list():
    address = input('Enter products sitemap path (HTTP/HTTPS is required): ')
    if address.startswith('https://') or address.startswith('http://'):
        print(get_products_list([address]))
    else:
        print("Invalid address. Must start with HTTP/HTTPS.")

def handle_products_info():
    address = input('Enter products sitemap path (HTTP/HTTPS is required): ')
    if address.startswith('https://') or address.startswith('http://'):
        print(get_product_info([address]))
    else:
        print("Invalid address. Must start with HTTP/HTTPS.")

def handle_test():
    address = input('Enter valid address (HTTP/HTTPS is required): ')
    if address.startswith('https://') or address.startswith('http://'):
        test(address)
    else:
        print("Invalid address. Must start with HTTP/HTTPS.")
