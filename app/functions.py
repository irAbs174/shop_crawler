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