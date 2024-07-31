from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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

def scroll_and_load(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_products_sitemap(soup):
    if soup is None:
        return []

    product_sitemaps = []
    for i in soup.select('sitemap'):
        if 'product-sitemap' in i.loc.text:
            product_sitemaps.append(i.loc.text)
    return product_sitemaps

def get_products_list(products_sitemap_list, ua):
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
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(product_address)
        scroll_and_load(driver)
        btn = driver.find_elements(By.XPATH, "//button[contains(@class, 'single_add_to_cart_button') and @disabled]")
        driver.close()
        print(f'btn +>>> {btn}')
        if btn == []:
            is_available = False
        else:
            is_available = True

        headers = {'User-Agent': ua.random}
        content_html = crawler(product_address, headers=headers)
    
        if content_html is None:
            return None

        product_name = content_html.title.text
    
        if is_available:
            return {
                'name': product_name,
                'price': 0,
                'status': 'ناموجود',
                }
        else:
            # Extract and convert price
            price_element = content_html.find(class_='woocommerce-Price-amount amount')
            price_text = price_element.text
            price_digits = re.sub(r'[^\d]', '', price_text)
            if price_digits.isdigit():
                price = int(price_digits) * 4
            else:
                price = '0'  # Price not found or invalid
            
            return {
                'name': product_name,
                'price': price,
                'status': 'موجود',
            }

    except Exception as e:
        print(e)
