from bs4 import BeautifulSoup as bs4
import requests as R
 
def crawl(target):
    target_html = R.get(target).text
    target_soup = bs4(target_html, 'html.parser')
    return target_soup
 
def products_sitemap(soup):
    list = []
    for i in soup.select('sitemap'):
        if 'product-sitemap' in i.loc.text:
            list.append(i.loc.text)
        
    
    return list

def products_list(products_sitemap_list):
    list = []
    for i in products_sitemap_list:
        soup = crawl(i)
        urls = soup.select('url')
        for j in urls:
            if 'webp' or 'jpg' or 'png' or 'jpeg' in j.text:
                list.append(j.loc.text)
                    
            
    
    return list

def main():
    print('SHOP CRAWLER version 0.0.1\ndeveloper => UNIQUE174\n')
    target = input("Enter target(https required): ")
    if 'https://' in target:
        target_sitemap_soup = crawl(f'{target}/sitemap_index.xml')
        products_sitemap_list = products_sitemap(target_sitemap_soup)
        target_products = products_list(products_sitemap_list)
        print(f'All products => {len(target_products)}')

        fclt_list = []

        for i in target_products:
            if 'fclt' in i :
                fclt_list.append(i)
    
        print(f'Forward Products => {len(fclt_list)}')
    elif target == 'exit':
        print('GOODBYE! \n')
        exit()
    else:
        print('Error 0 => Please enter valid url (https required) \n')

if __name__ == '__main__':
    while 1:
        main()

