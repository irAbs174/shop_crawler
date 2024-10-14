from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore
import requests as R
import logging
import time
import re


logging.basicConfig(filename='scraper.log', level=logging.ERROR)

def crawler(target, headers, retries=3):
    for _ in range(retries):
        try:
            target_html = R.get(target, headers=headers).text
            target_soup = bs4(target_html, 'html.parser')
            return target_soup
        except Exception as e:
            logging.error(f"Error fetching {target}: {e}")
            time.sleep(5)  # Wait for a few seconds before retrying
    return None

def get_products_sitemap(soup):
    print(Fore.YELLOW)
    if soup is None:
        return []
    
    product_sitemaps = []
    for i in soup.select('sitemap'):
        if 'product-sitemap' in i.loc.text:
            product_sitemaps.append(i.loc.text)
    return product_sitemaps

def get_products_list(products_sitemap_list, ua):
    print(Fore.RED)
    products_list = []
    headers = {'User-Agent': ua.random}
    for i in products_sitemap_list:
        soup = crawler(i, headers=headers)
        if soup:
            urls = soup.select('url')
            for j in urls:
                if any(ext in j.text for ext in ['.webp', '.jpg', '.png', '.jpeg']):
                    products_list.append(j.loc.text)
    return products_list

def get_product_info(product_address, ua):
    print(Fore.GREEN)
    content_html = bs4(R.get(product_address).text, 'html.parser')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver = webdriver.Chrome()
    driver.get(product_address)
    try:
        if 'buy' in product_address:
            soup = bs4(driver.page_source, "html.parser")
            variations_data = soup.find('form', {'class': 'variations_form cart'})['data-product_variations']
            variations_data = variations_data.replace('&quot;', '"').replace('\\/', '/')
            variations = variations_data.split('},{')
            color_quantity = []
            all_unavailable = True
            for variation in variations:
                variation = variation.replace('{', '').replace('}', '')
                color_start = variation.find('attribute_pa_color') + len('attribute_pa_color":"')
                color_end = variation.find('"', color_start)
                color = variation[color_start:color_end]
                availability_start = variation.find('availability_html') + len('availability_html":"')
                availability_end = variation.find('<', availability_start)
                availability = variation[availability_start:availability_end]
                price_start = variation.find('display_price') + len('display_price":')
                price_end = variation.find(',', price_start)
                price = variation[price_start:price_end]
                regular_price_start = variation.find('display_regular_price') + len('display_regular_price":')
                regular_price_end = variation.find(',', regular_price_start)
                regular_price = variation[regular_price_start:regular_price_end]
                max_qty_start = variation.find('max_qty') + len('max_qty":')
                max_qty_end = variation.find(',', max_qty_start)
                max_qty = variation[max_qty_start:max_qty_end]
                if max_qty != "":
                    all_unavailable = False
                
                color_quantity.append({
                    'color':color,
                    'quantity' : "Ù†Ø§Ù…ÙˆØ¬ÙˆØ¯" if max_qty == '""' else max_qty
                    })
            payload =  {
                    "name": driver.title,
                    "price": regular_price,
                    "status": {'color':'', 'quantity':"Ù†Ø§Ù…ÙˆØ¬ÙˆØ¯" if all_unavailable else color_quantity}
                    }
            driver.quit()
            return payload

        elif '123' in product_address:
            product_name = driver.title
            content_html = bs4(driver.page_source, "html.parser")
            stock = content_html.select('p.out-of-stock')

            if stock == []:
                price_element = content_html.select('bdi')[1].text
                persian_number = price_element.split('\xa0')[0]
                # Translation table: Persian digits to Arabic numerals
                translation_table = str.maketrans('Û°Û±Û²Û³Û´ÛµÛ¶Û·Û¸Û¹', '0123456789')
                # Convert Persian digits to Arabic numerals
                arabic_number = persian_number.translate(translation_table)
                # Remove any thousand separators
                arabic_number = arabic_number.replace(',', '')
                # Convert to integer
                number = int(arabic_number)
                
                return {
                    'name': product_name,
                    'price': number,
                    'status' : [{"color": "", "quantity":"Ù…ÙˆØ¬ÙˆØ¯"}],
                }
            else:
                return {
                    'name': product_name,
                    'price': 0,
                    'status' : [{"color": "", "quantity":"Ù†Ø§Ù…ÙˆØ¬ÙˆØ¯"}],
                    }

        elif 'kifche' in product_address:
            product_name = content_html.title.text
            print('KIFCHE')
            return {
                'name': product_name,
                'price': 0,
                'status': [{"color": "", "quantity":""}],
            }
        elif 'snapshop' in product_address:
            pass
        elif 'digikala' in product_address:
            pass
        else:
            pass
    

    except Exception as e:
        print(e)