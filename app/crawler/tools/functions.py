from bs4 import BeautifulSoup as bs4
import requests as R
import logging
import time
import re


logging.basicConfig(filename='scraper.log', level=logging.ERROR)

def crawler(target, retries=3):
    for _ in range(retries):
        try:
            target_html = R.get(target).text
            target_soup = bs4(target_html, 'html.parser')
            return target_soup
        except Exception as e:
            logging.error(f"Error fetching {target}: {e}")
            time.sleep(5)  # Wait for a few seconds before retrying
    return None

def get_products_sitemap(soup):
    if soup is None:
        return []

    product_sitemaps = []
    for i in soup.select('sitemap'):
        if 'product-sitemap' in i.loc.text:
            product_sitemaps.append(i.loc.text)
    return product_sitemaps

def get_products_list(products_sitemap_list):
    products_list = []
    for i in products_sitemap_list:
        soup = crawler(i)
        if soup:
            urls = soup.select('url')
            for j in urls:
                if any(ext in j.text for ext in ['.webp', '.jpg', '.png', '.jpeg']):
                    products_list.append(j.loc.text)
    return products_list

def get_product_info(product_address):
    content_html = crawler(product_address)
    
    if content_html is None:
        return None
    
    # Extract product name
    product_name = content_html.title.text
    
    # Check availability
    try:
        is_available = content_html.select('span.out_stock')[0].text
    except:
        is_available = 'موجود'
    if is_available == 'ناموجود ':
        return {
            'name': product_name,
            'price': 0,
            'status': 'ناموجود',
        }
    else:
        # Extract and convert price
        price_element = content_html.find(class_='woocommerce-Price-amount amount')
        if price_element and price_element.text != 'تماس بگیرید':
            price_text = price_element.text
            price_digits = re.sub(r'[^\d]', '', price_text)
            if price_digits.isdigit():
                price = int(price_digits) * 4
            else:
                price = 'ناموجود'  # Price not found or invalid
        else:
            price = 'ناموجود'  # Price element not found
        
        return {
            'name': product_name,
            'price': price,
            'status': 'موجود',
        }
    
def main_dic_modify(products_list):
    main_dic = []
    try:
        for product_address in products_list:
            product_info = get_product_info(product_address)
            if product_info:
                print(product_info)
                main_dic.append(product_info)
    except AttributeError as e:
        print(e)
        return None
    return main_dic

def comparison(name, price, main_dic):
    status = ''
    try:
        for i in main_dic:
            if name in i['name']:
                if i['price'] < price:
                    status = 'down'
                elif i['price'] == price:
                    status = 'equals'
        
        return status
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Test function:
def serve():
    address = input("Enter address: \n")
    target_dic = {}
    product_name = ''

    while product_name != 'start':
        # give me required data
        product_name = input('enter product name:')
        product_price = input('enter product price:')
        target_dic[product_name] = int(product_price)

    sitemap_soup = crawler(f'{address}/sitemap_index.xml')
    if sitemap_soup:
        #product_sitemaps = get_products_sitemap(sitemap_soup)
        #products_list = get_products_list(product_sitemaps)
        #main_dic_modify(product_sitemaps)
        main_dic = [
            {'name': 'کوله پشتی لپتاپ Catesigo مدل C13386 - بای کیف', 'price': 2599000, 'status': 'موجود'},
            {'name': 'کوله پشتی لپتاپ Catesigo مدل C13387 - بای کیف', 'price': 2599000, 'status': 'موجود'}
        ]
        for i in target_dic:
            status = comparison(i, target_dic[i], main_dic)
            if status == 'down':
                print(f'=> The {i} product is down !')
            elif status == 'equals':
                print(f'=> The {i} product is equals !')

# Test function:
def test(address):
    sitemap_soup = crawler(f'{address}/sitemap_index.xml')
    if sitemap_soup:
        product_sitemaps = get_products_sitemap(sitemap_soup)
        products_list = get_products_list(product_sitemaps)
        for product_address in products_list:
            product_info = get_product_info(product_address)
            if product_info:
                print(product_info)