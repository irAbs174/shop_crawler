import requests
from openpyxl import Workbook

# Create a new Workbook
wb = Workbook()

# Select the active worksheet
ws = wb.active

def export_products():
    response = requests.post('http://0.0.0.0:8080/api/get_products_api', data={})
    data = [[
        'فروشگاه',
        'نام کالا',
        'قیمت کالا',
        'وضعیت',
        'موجودی',
        'صفحه محصول',
    ]]
    for i in response.json()['status']:
        if i['price'] == '0':
            stock = 'ناموجود'
        elif i['stock'] == 'ناموجود':
            stock = 'ناموجود'
        else:
            stock = 'موجود'
        data.append([
            i['parent'],
            i['name'],
            i['price'],
            i['status'],
            stock,
            i['url'],
        ])

                    # Write data to the worksheet
        for row in data:
            print(row)
            ws.append(row)
        
        # Save the Workbook to a file
        file_path = 'media/products.xlsx'
        wb.save(file_path)