import csv
from colorama import Fore
import requests
import time

def clean_stock_data(stock_data):
    """Cleans the 'موجودی' column data."""
    # Initialize a list to hold cleaned stock entries
    cleaned_stock = []
    
    # Parse each stock item
    for stock_item in stock_data.get('quantity', []):
        color = stock_item.get('color', '')
        quantity = stock_item.get('quantity', '')
        if color and quantity:
            # Format each entry as 'color: quantity'
            cleaned_stock.append(f"{color}: {quantity}")
    
    # Join all cleaned entries into a single string, separated by commas
    return ', '.join(cleaned_stock)

while True:
    print(Fore.RED, "START EXPORT")
    fields = ['فروشگاه', 'نام محصول', 'قیمت', 'موجودی', 'آدرس محصول']
    rows = []
    
    response = requests.post('http://0.0.0.0:8080/api/get_products_api', data={})
    if response.json().get('status'):
        for product in response.json()['status']:
            print(Fore.BLUE, product)
            
            # Clean the 'موجودی' data before adding it to the rows
            cleaned_stock = clean_stock_data(product.get('stock', {}))
            
            rows.append([
                product['parent'],
                f"{product['name']}",
                product['price'],
                cleaned_stock,  # Insert the cleaned stock data here
                product['url'],
            ])
        
    # Name of the CSV file
    filename = f"Products_Export.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Creating a CSV writer object
        csvwriter = csv.writer(csvfile)

        # Writing the fields
        csvwriter.writerow(fields)

        # Writing the data rows
        csvwriter.writerows(rows)

    print(Fore.GREEN, 'EXPORTED SUCCESSFULLY!')
    
    # Sleep for 60 seconds
    for i in range(60):
        print(Fore.YELLOW, f"Sleeping ... {i} second(s)!\n")
        time.sleep(1)
