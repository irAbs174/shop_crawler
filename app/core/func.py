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

    content_html = bs4(R.get(product_address).text, 'html.parser')

    stock = content_html.select('p.out-of-stock')

    try:
        if '123kif' in product_address:

            if content_html is None:
                return None

            product_name = content_html.title.text

            if stock == []:
                print("MOJOD")
                # Extract and convert price
                price_element = content_html.select('bdi')[1].text
                print(price_element)
                persian_number = price_element.split('\xa0')[0]
                print(persian_number)
                # Translation table: Persian digits to Arabic numerals
                translation_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
                print(translation_table)
                # Convert Persian digits to Arabic numerals
                arabic_number = persian_number.translate(translation_table)
                print(arabic_number)
                # Remove any thousand separators
                arabic_number = arabic_number.replace(',', '')
                print(arabic_number)
                # Convert to integer
                number = int(arabic_number)
                
                return {
                    'name': product_name,
                    'price': number,
                    'status': 'موجود',
                }
            else:
                print("NAMOJOD")
                return {
                    'name': product_name,
                    'price': 0,
                    'status': 'ناموجود',
                    }
        elif 'buykif' in product_address:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
                if stock != []:
                    if stock[0].text == 'متاسفانه این محصول در حال حاضر موجود نمی باشد. می توانید از لیست پایین همین برگه، محصولات مشابه آن را مشاهده کنید.':
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
        elif 'kifche' in product_address:
            product_name = content_html.title.text
            print('KIFCHE')
            return {
                'name': product_name,
                'price': 0,
                'status': 'موجود',
            }
        elif 'snapshop' in product_address:
            pass
        elif 'digikala' in product_address:
            pass
        else:
            pass
    

    except Exception as e:
        print(e)
