import json
import os

dir_in='C:\\Users\\quasar\\invoice_handling\\2021\\iunie\\18\\5_VALIDATE_INVOICE\\'
dir_out='C:\\Users\\quasar\\invoice_handling\\2021\\iunie\\charisma\\'
for file in os.listdir('C:\\Users\\quasar\\invoice_handling\\2021\\iunie\\18\\5_VALIDATE_INVOICE\\'):
    with open(dir_in+str(file), 'rb') as json_file:
        data = json.load(json_file)

    data_charisma={
        "supplierpartnerCUI": data['Furnizor']['cod'],
	    "supplierpartnerName": data['denumire_firma'],
        "contIBAN": data['Furnizor']['IBAN'],
        "customerpartnerCUI": data['Client']['IBAN'],
        "customerpartnerName": data['grup'],
        "serialNo": "ImpMed",
        "invoiceNumber": data['numar_factura'],
        "invoiceDate": data['data'],
        "paymentDate": "2021-03-02",
        "paymentValue":  data['total'],	
        "invoiceDescription": data['nume_factura'],
    }


    with open (dir_out+str(file), 'w') as write:
        json.dump(data_charisma, write, indent=4)