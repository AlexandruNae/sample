import requests, json, os
from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth 
from pprint import pprint 
import os

import requests
import json
from datetime import date, timedelta
import sys
import datetime
import os
from datetime import date, timedelta

now = datetime.datetime.now()
folder_an = now.year
folder_luna = now.month
folder_zi = now.day

dict_numar_nume_luna = {
  "1": "ianuarie",
  "2": "februarie",
  "3": "martie",
  "4": "aprilie",
  "5": "mai",
  "6": "iunie",
  "7": "iulie",
  "8": "august",
  "9": "septembrie",
  "10": "octombrie",
  "11": "noiembrie",
  "12": "decembrie"
}
nume_luna = dict_numar_nume_luna[str(folder_luna)]
folder = str(folder_an) + "\\" + nume_luna + "\\" + str(folder_zi)

es_index = nume_luna + "_" + str(folder_zi)

username = 'elastic'
password = 'elastic'

headers = {"Content-Type":"application/json", "Authorization": "Basic ZWxhc3RpYzplbGFzdGlj"}

directory_error = 'C:\\Users\\quasar\\invoice_handling\\'+folder+'\\4_VALIDATE_ERROR\\'
directory_pass = 'C:\\Users\\quasar\\invoice_handling\\'+folder+'\\5_VALIDATE_INVOICE\\'

# processed_error = 'C:\\Users\\quasar\\invoice_handling\\Noiembrie_15\\4.1_VALIDATE_ERROR_UPLOADED\\'
# processed_pass = 'C:\\Users\\quasar\\invoice_handling\\Noiembrie_15\\5.1_VALIDATE_INVOICE_UPLOADED\\'

urlInvoiceStatus="http://192.168.0.39:9200/"+es_index+"_error/doc"
count = 0
for file in os.listdir(directory_error):
    count = count + 1
    with open(directory_error+file) as json_file :
        query = json.load(json_file)
        # info = json.loads(js.decode("utf-8"))
    print(file)
    data = requests.post(url=urlInvoiceStatus, headers=headers, json=query)
    print(data)


print(count)
urlInvoiceStatus="http://192.168.0.39:9200/"+es_index+"_pass/doc"
for file in os.listdir(directory_pass):
    with open(directory_pass+file) as json_file :
        query = json.load(json_file)
        # info = json.loads(js.decode("utf-8"))
    print(file)
    data = requests.post(url=urlInvoiceStatus, headers=headers, json=query)
    print(data)



#     # response = requests.get('http://192.168.0.39:9200/invoicestatus_test', auth = HTTPBasicAuth(username, password))
#     # pprint(response.content)

# for file in os.listdir(directory_error):
#     os.rename(directory_error+file, processed_error+file)

# for file in os.listdir(directory_pass):
#     os.rename(directory_pass+file, processed_pass+file)