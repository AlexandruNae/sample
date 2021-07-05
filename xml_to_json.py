# import xmltodict, json
folder = 'C:\\Users\\quasar\\invoice_handling\\2021\\iunie\\xml2\\3.0_INVOICE_JSON\\'
folder_fisier = 'C:\\Users\\quasar\\invoice_handling\\2021\\iunie\\xml2\\'
xml = folder_fisier+'facturi interne luna mai 2021.xml'

# o = xmltodict.parse(xml)
# s = json.dumps(o) # '{"e": {"a": ["text", "text"]}}'
# print(s)




import xml.etree.ElementTree as ET
import xmltodict
import json


tree = ET.parse(xml)
xml_data = tree.getroot()
#here you can change the encoding type to be able to set it to the one you need
xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

data_dict = dict(xmltodict.parse(xmlstr))
s = json.dumps(data_dict)

i=0
for record in data_dict['facturirm']['record']:

    numar_string = data_dict['facturirm']['record'][i]['Nrfact_FACT']
    numar = ''
    print("numar string",numar_string)
    if " " in numar_string:
        for c in numar_string.split():
            if c.isdigit():
                numar= numar+c
    else:
         for c in numar_string:
            if c.isdigit():
                numar= numar+c
    print("numar",numar)

    data = data_dict['facturirm']['record'][i]['Datafactura']
    data = data[-2:] + '/' + data[5:7] + '/' +data[:4]

    factura ={"Furnizor": {
            "Nume": data_dict['facturirm']['record'][i]['Numefurnizor'],
            "cod": data_dict['facturirm']['record'][i]['CIFFRZ'],
            "IBAN": data_dict['facturirm']['record'][i]['IBAN'],

        },
            "Client": {
                "Nume": data_dict['facturirm']['record'][i]['Client'],
                "cod": data_dict['facturirm']['record'][i]['CUIclient'],
                "IBAN": data_dict['facturirm']['record'][i]['CONTBANCARclient'],

            },
            "total": data_dict['facturirm']['record'][i]['Sumadefacturat'],
            "numar_factura": numar,
            "data": data, 
            "nume_factura": "contradiction"
        }
    with open (folder + str(i+1) +'.json', 'w') as out:
        json.dump(factura, out, indent = 4)
        print(i+1)
    i = i+1

# with open ('C:\\Users\\quasar\\invoice_handling\\2021\\xml\\out.json', 'w') as out:
#     json.dump(data_dict, out, indent = 4)


