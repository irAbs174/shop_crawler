from colorama import Fore, Style
import requests
import json
import csv


class Export:
    def __init__(self, jobArg):
        print(Fore.BLUE, "START EXPORT ALL PRODUCTS ...")
        self.fields = ['فروشگاه', 'نام محصول', 'قیمت', 'موجودی', 'آدرس محصول']
        self.jobArg = jobArg

    def str_to_json(self, x):
        try:
            self.qc = json.loads(x.replace("'", '"').replace('\n', ''))
        except Exception as error:
            self.qc = {}
            print(Fore.RED, f"Error: {error}")
        
    def export(self):
        payload = {
                'jobArg' : self.jobArg
                }
        response = requests.post('http://0.0.0.0:8080/api/get_products_api', payload)
        rows = []
        for i in response.json()['status']:
            self.str_to_json(i['stock'])
            for j in self.qc:
                rows.append([
                    i['parent'],
                    f"{i['name']} - {j['color']}",
                    i['price'],
                    j['quantity'],
                    i['url'],
                    ])
                
        
        # name of csv file
        filename = f"Export_{self.jobArg}.csv"
        for i in rows:
            print(Fore.GREEN, f"=>  {i}   <=")
        
        # writing to csv file
        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(self.fields)
            # writing the data rows
            csvwriter.writerows(rows)
            
        print(Fore.YELLOW, f'=> EXPORT GENERATED SECCESSFULY TO > Export_{self.jobArg}.csv FILE')
        print(Style.RESET_ALL)


if __name__ == "__main__":
    Export('All').export()