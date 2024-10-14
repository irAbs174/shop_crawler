from colorama import Fore, Style
import requests
import json
import csv


class Export:
    def __init__(self, jobArg):
        print(Fore.BLUE, "START EXPORT ALL PRODUCTS ...")
        self.fields = ['ÙØ±ÙˆØ´Ú¯Ø§Ù‡', 'Ù†Ø§Ù… Ù…Ø­ØµÙˆÙ„', 'Ù‚ÛŒÙ…Øª', 'Ù…ÙˆØ¬ÙˆØ¯ÛŒ', 'Ø¢Ø¯Ø±Ø³ Ù…Ø­ØµÙˆÙ„']
        self.rows = []
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
        response = requests.post('http://0.0.0.0:8080/api/get_products_api', data=payload)
        for i in response.json()['status']:
            self.str_to_json(i['stock'])
            for j in self.qc:
                self.rows.append([
                    i['parent'],
                    f"{i['name']} - {j['color']}",
                    i['price'],
                    j['quantity'],
                    i['url'],
                    ])
                
        
        # name of csv file
        filename = f"Export_{self.jobArg}.csv"
        for i in self.rows:
            print(Fore.GREEN, f"=>  {i}   <=")
        
        # writing to csv file
        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(self.fields)
            # writing the data rows
            csvwriter.writerows(self.rows)
            
        print(Fore.YELLOW, '=> EXPORT GENERATED SECCESSFULY TO > export.csv FILE')
        print(Style.RESET_ALL)


if __name__ == "__main__":
    Export('All').export()