from typing import Optional, Match
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from dateutil.parser import parse
import pdfminer
import math
import re
import collections
import json
import string
from datetime import datetime
from datetime import date
from dateutil import parser as dateparser
from datetime import timedelta
import random
today = datetime.today().strftime('%Y-%m-%d')

now = datetime.now()

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
# folder = str(folder_an) + "\\" + nume_luna + "\\test6"




# Open a PDF file.


def main(fp, numar, file):
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    text_boxes = []
    lista_secundara_furnizor = ["Furnizor", "furnizor", "FURNIZOR", "Furnizor:", "furnizor:", "FURNIZOR:"]
    lista_furnizor = ["Medical", "MEDICAL", "Medic", "MEDIC", "Medicina", "MEDICINA", "DR.", "DR", "Doctor", "DOCTOR"]
    lista_client = ["SRL", "S.R.L"]
    lista_CUI = ["cui", "c.u.i", "c.u.i.", "c.u.i.:", "cui:", "c.u.i:", "cif", "c.i.f", "c.i.f.", "c.i.f.:", "cif:",
                 "c.i.f:", "cif/cui","cui/cif", "c.u.i/c.i.f:", "cifcui", "cuicif", "cf/cu|", "cf/cui",
                 "c.u.i/c.i.f:","c.u.i/c.i.f", "cui/c.i.f:","c.u.i/cif", 'c.u.i/cif:', 'c.u.i/c.i.f', 'cficui', '.c.i.f', "cod",
                 "fiscal","Tax ID :"]

    lista_CUI_client = ["15710936","RO15710936", "18463202", "RO5919324","5919324", "RO18463202","18463202", "RO14009050","14009050", 
                        "27590027", "14105023", "RO27590027", "RO14105023", "29410661", "33370956", "RO29410661", "RO33370956",
                        "28353290", "RO26630352", "2610501", "16491486", "24454900", "R O24469080", "29114763", "18164472", "22183847", 
                        "RO28353290", "26630352", "RO2610501", "RO16491486", "RO24454900", "24469080", "RO29114763", "RO18164472", 
                        "RO22183847","19216537", "25109543", "35621094", "22355713", "17002740", "29290603", "30157091", "RO19216537", 
                        "RO25109543", "RO35621094", "RO22355713", "RO17002740", "RO29290603", "RO30157091", '29290603', 'RO29290603',
                        '2610501', 'RO2610501']

    lista_IBAN_client = [  'RO33RZBR0000060013094217', 'RO57RZBR0000060011686315', 'RO30BTRLRONCRT0336557301', 'RO25INGB0021000054408911',
                           'RO07BTRL0140120288827XX',  'RO64BUCU1611215952081RON', 'RO13BTRL04301202169300RON','RO68BTRL01301202P19088XX', 
                           'RO36BTRL01301202L81010XX', 'RO31BTRL00501202H56948XX', 'RO63BTRLRONCRT0231244001', 'RO02RZBR0000060009280541',
                           'RO31BTRL01301202615808XX', 'RO15OTPV0000000002625129', 'RO98BTRL00501202H56948XX', 'RO27BTRL01301202955316XX',
                           'RO32RZBR0000060012181950', 'RO17RZBR0000060006520136', 'RO13BTRL04301202169300XX',
                           'RO21TREZ2315069XXX031484', 'RO09BTRLONCRT0221692801', 'RO51BTRL02701202T86156XX',
                           'RO11BTRL02701202K46888XX', 'RO92INGB0001008183858910', 'RO12BUCU1311215937904RON', 'RO16TREZ0625069XXX005192',
                           'RO78RZBR0000060013966019', 'RO09BTRLRONCRT0221692801', 'RO62DAFB101800157448RO01', 'RO33RZBR0000060013094210', 'RO17BTRLRONCRT0261331901']

    lista_stop_nume = ["RC ", "J ", "RCJ", "CUI", "C.U.I", "CUI:" , "C.U.I:", "CIF", "C.I.F", "C.I.F.", "C.I.F.:",
                       "CIF:", "C.I.F:", "Sediu", "SEDIU", "sediu"]
    lista_factura = ["Serie", "Seria", "SERIA", "SERIE", "Factura", "FACTURA", "factura"]
    lista_ron = ["Lei", "lei", "LEI", "ron", "RON"]
    lista_total = [ "total", "valoare", "valoarea","-lei-"]
    
    dictionar_luni = { "01": "ia", "02" :"fe", "03": "mar", "04": "ap", "05":"mai", "06":"iun", "07": "iul", "08": "au", "09": "se", 
                       "10": "oc", "11": "no", "12": "de"}

    dictionar_luni_en = { "01": "ja", "02" :"fe", "03": "mar", "04": "ap", "05":"may", "06":"jun", "07": "jul", "08": "au", "09": "se", 
                       "10": "oc", "11": "no", "12": "de"}

    luni_helper = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie']

    class Boxes:
        def __init__(self, x_sj, y_sj, x_ds, y_ds, text):
            self.x_sj = x_sj
            self.y_sj = y_sj
            self.x_ds = x_ds
            self.y_ds = y_ds
            self.x_centru = (x_sj + x_ds) / 2
            self.y_centru = (y_sj + y_ds) / 2
            self.text = text




    def parse_obj(lt_objs):
        contor = 0

        for obj in lt_objs:

            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBox):

                text_boxes.append(
                    Boxes(obj.bbox[0], obj.bbox[1], obj.bbox[2], obj.bbox[3], obj.get_text().replace('\n', ' ')))
                print({"x": obj.bbox[0], "y": obj.bbox[1], "text": obj.get_text().replace('\n', ' ')})
                contor = contor + 1


            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                parse_obj(obj._objs)


        return contor

    # loop over all pages in the document
    for page in PDFPage.create_pages(document):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        contor = parse_obj(layout._objs)

    # Verificare factura
    words_verificare = []
    words_legate = ''
    for i in range(0, len(text_boxes)):
        words_temp = text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').split()
        for j in range(0, len(words_temp)):
            words_verificare.append(words_temp[j])
            words_legate = words_legate + words_temp[j]
    
    if 'factura' not in words_verificare and 'factură' not in words_verificare and 'factura' not in words_legate and 'factură' not in words_legate: # SI 'chitanta' in  ?????????????
        return print(file + ' ---> NU E FACTURA !!! 1 ')
        

    try: 
        for i in range(len(words_verificare)):
            if words_verificare[i] =='raport' and words_verificare[i+1] == 'activitate' and words_verificare[i+2] == 'luna' and 'executii' in words_verificare and 'investigatie' in words_verificare:
                return print(file + ' ---> NU E FACTURA !!! 2')
    except IndexError:
        pass

    # print(words_verificare)
    try: 
        for i in range(len(words_verificare)):
            if words_verificare[i] =='situatie' and words_verificare[i+1] == 'plata' and words_verificare[i+2] == 'med.' and words_verificare[i+3] == 'int.':
                return print(file + ' ---> NU E FACTURA !!! 3')
    except IndexError:
        pass

    try:
        if file.lower().startswith('polita') or file.lower().startswith('pontaj') or file.lower().startswith('viza') or file.lower().startswith('asigurare') or file.lower().startswith('malpraxis'):
            return print(file + ' ---> NU E FACTURA !!! 4')
    except Exception:
        pass

    def distanta(x1, y1, x2, y2):
        return math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))

    index_box_furnizor = -1
    index_box_client = -1
    search_array = []
    factura_furnizor_nume = ''
    factura_client_nume = ''

    def search_furnizor(x_sj_box, y_sj_box):
        for i in range(0, contor):
            search_array.append({"Euclidian": distanta(x_sj_box, y_sj_box, text_boxes[i].x_sj, text_boxes[i].y_sj),
                                 "Value": text_boxes[i].text
                                 })
        for i in range(len(search_array)):
            if search_array[i]["Value"] == '':
                search_array[i]["Euclidian"] = search_array[i]["Euclidian"] * 10
        for i in range(0, contor):
            for j in range(0, len(lista_furnizor)):
                if lista_furnizor[j] in search_array[i]["Value"]:
                    factura_furnizor_nume = search_array[i]["Value"]
                    return factura_furnizor_nume

    search_array.clear()

    def search_client(x_sj_box, y_sj_box):
        for i in range(0, contor):
            search_array.append({"Euclidian": distanta(x_sj_box, y_sj_box, text_boxes[i].x_sj, text_boxes[i].y_sj),
                                 "Value": text_boxes[i].text
                                 })
        for i in range(len(search_array)):
            if search_array[i]["Value"] == '':
                search_array[i]["Euclidian"] = search_array[i]["Euclidian"] * 10
        for i in range(0, contor):
            for j in range(0, len(lista_client)):
                if lista_client[j] in search_array[i]["Value"]:
                    if search_array[i]["Value"] != search_furnizor(text_boxes[index_box_furnizor].x_sj,
                                                                   text_boxes[index_box_furnizor].y_sj):
                        factura_client_nume = search_array[i]["Value"]
                        return factura_client_nume


    try:
        box_furnizor = search_furnizor(text_boxes[index_box_furnizor].x_sj, text_boxes[index_box_furnizor].y_sj)
        box_client = search_client(text_boxes[index_box_client].x_sj, text_boxes[index_box_client].y_sj)
    except IndexError:
        print(file)
        print("IndexError")
        return

    res = []
    for i in range(0, len(lista_stop_nume)):
        if box_furnizor is not None:
            res.append(box_furnizor.partition(lista_stop_nume[i])[0])
            lista_furnizor_nume = sorted(res, key=len)
            if lista_furnizor_nume is not None:
                factura_furnizor_nume = lista_furnizor_nume[0]

    res_1 = []
    for i in range(0, len(lista_stop_nume)):
        if box_client is not None:
            res_1.append(box_client.partition(lista_stop_nume[i])[0])
            lista_client_nume = sorted(res_1, key=len)
            if lista_client_nume is not None:
                factura_client_nume = lista_client_nume[0]


    def validate_CUI(cui):
        
        if len(cui) > 10 or len(cui) < 6:
            return False

        if cui=='000000' or cui=='0000000' or cui=='00000000' or cui=='000000000':
            return False


        if isinstance(cui, str):
            if "ro" == cui[:2] or "RO" == cui[:2] or "Ro" == cui[:2]:
                cui = cui[2:]
        try:
            cui_var = int(cui)
        except TypeError:
            return False
        except ValueError:
            return False

        nr_control = 753217532

        cifra_control = cui_var % 10

        cui_var = int(cui_var / 10)

        t = 0

        for i in range(0, len(str(cui_var))):
            t += int(cui_var % 10) * int(nr_control % 10)
            cui_var = int(cui_var) / 10
            nr_control = int(nr_control / 10)

        cifra_control_2 = t * 10 % 11

        if cifra_control_2 == 10:
            cifra_control_2 = 0

        if (cifra_control == cifra_control_2):
            return True
        else:
            return False



    def CUI_furnizor():

        words = []
        position = [[0 for x in range(2)] for y in range(len(text_boxes))]

        for i in range(0, len(text_boxes)):
            words.append(text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace('..', ' ').replace('.', '').split())
            position[i][0] = text_boxes[i].x_centru
            position[i][1] = text_boxes[i].y_centru
        
        coordonate_helper = {}

        for i in range(len(words)):
            for j in range(len(words[i])):
                if words[i][j] in lista_CUI:
                    # print(words[i][j])
                    coordonate_helper[position[i][0]] = position[i][1]
                    break
            if coordonate_helper:
                break

        coordonate_helper_sorted = {k: coordonate_helper[k] for k in sorted(coordonate_helper)}
        values_coordonate_helper_sorted = list(coordonate_helper_sorted.values())
        coordonate_cui = []
        try:
            coordonate_cui.append(list(coordonate_helper_sorted.keys())[0])
            coordonate_cui.append(values_coordonate_helper_sorted[0])
        except IndexError:
            pass

        dict_distante_pozitii = {}

        try:
            for i in range(0, len(text_boxes)):
                dict_distante_pozitii[math.sqrt(pow((position[i][0] - coordonate_cui[0]), 2) + pow((position[i][1] - coordonate_cui[1]), 2))] = text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace(';', ' ').replace('.r', 'r').replace('"', ' ').replace('.', ' ').split()
        except IndexError:
            print(file)
            print("index error line 281")
        sorted_dict = {k: dict_distante_pozitii[k] for k in sorted(dict_distante_pozitii)}
        values = list(sorted_dict.values())
        cui_furnizor = ''

        # print('ASADAR', validate_CUI('1275530'))
        # for i in range(len(values)):
        #     for j in range(len(values[i])):
        #         if validate_CUI(values[i][j]):
        #             print(values[i][j])
        # print(values)

        for i in range(len(values)):
            for j in range(len(values[i])):
                if validate_CUI(values[i][j]) and values[i][j].upper() not in lista_CUI_client:
                    # print(values[i][j])
                    try:
                        if values[i][j-1]=='ro':
                            cui_furnizor = values[i][j-1] + values[i][j]
                            break
                    except IndexError:
                        pass
                    if not cui_furnizor:
                        try:
                            if(values[i][j+1] == 'ro' + values[i][j]):
                                cui_furnizor = values[i][j+1]
                        except IndexError:
                            pass
                        if not cui_furnizor and values[i][j].upper() not in lista_CUI_client :
                            # print(validate_CUI(values[i][j+1]), values[i][j+1])
                            cui_furnizor = values[i][j]
                            #caz special pentru FacturaA0025-CENTRUL-MEDICAL-UNIREA-SRL.pdf_0
                            try:
                                if validate_CUI(values[i][j+1]) and values[0] == ['reg', 'com', 'cif', 'adresa']:
                                    cui_furnizor = values[i][j+1]
                            except IndexError:
                                pass
                        break
            if cui_furnizor:
                break
        # print(cui_furnizor)
        return cui_furnizor.upper()

    CUI_furnizor = CUI_furnizor()

    def CUI_client():

        words = []
        position = [[0 for x in range(2)] for y in range(len(text_boxes))]

        for i in range(0, len(text_boxes)):
            words.append(text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace('..', ' ').replace('.', '').split())
            position[i][0] = text_boxes[i].x_centru
            position[i][1] = text_boxes[i].y_centru

        coordonate_helper = {}

        for i in range(len(words)):
            for j in range(len(words[i])):
                if words[i][j] in lista_CUI:
                    coordonate_helper[position[i][0]] = position[i][1]


        coordonate_helper_sorted = {k: coordonate_helper[k] for k in sorted(coordonate_helper, reverse=True)}
        values_coordonate_helper_sorted = list(coordonate_helper_sorted.values())
        coordonate_cui = []
        try:
            coordonate_cui.append(list(coordonate_helper_sorted.keys())[0])
            coordonate_cui.append(values_coordonate_helper_sorted[0])
        except IndexError:
            pass

        dict_distante_pozitii = {}

        try:
            for i in range(0, len(text_boxes)):
                dict_distante_pozitii[math.sqrt(pow((position[i][0] - coordonate_cui[0]), 2) + pow((position[i][1] - coordonate_cui[1]), 2))] = text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace(';', ' ').replace('.r', 'r').replace('"', ' ').replace('.', ' ').split()
        except IndexError:
            print("index error line 281")
        sorted_dict = {k: dict_distante_pozitii[k] for k in sorted(dict_distante_pozitii)}
        values = list(sorted_dict.values())
        
        cui_furnizor = ''
        
        cui_f_temp = CUI_furnizor.lower()

        # print('aaa',cui_f_temp[2:])
        # print(words)
        # print(values)
        for i in range(len(values)):
            for j in range(len(values[i])):
                if validate_CUI(values[i][j]) and values[i][j] != cui_f_temp and values[i][j] != cui_f_temp[2:] :
                    if values[i][j-1]=='ro' and (cui_f_temp!=values[i][j-1] + values[i][j]):
                        # print('bau')
                        cui_furnizor = values[i][j-1] + values[i][j]
                        break
                    if not cui_furnizor and values[i][j] in lista_CUI_client:
                        cui_furnizor = values[i][j]
                        break
            if cui_furnizor:
                break
        if not cui_furnizor:        
            for i in range(len(values)):
                for j in range(len(values[i])):
                    for k in range(len(lista_CUI_client)):
                        if values[i][j][-6:] == lista_CUI_client[k][-6:]:
                            cui_furnizor = lista_CUI_client[k]
                            break
        if cui_furnizor.startswith('roro'):
            cui_furnizor = cui_furnizor[2:]
        # print(cui_furnizor)

        if cui_furnizor.upper() not in lista_CUI_client:
            for i in range(len(values)):
                for j in range(len(values[i])):
                    if values[i][j].upper() in lista_CUI_client:
                        cui_furnizor = values[i][j].upper()

        return cui_furnizor.upper()

    CUI_client = CUI_client()
    
    # if not CUI_client and '30197091' in words_verificare:
    #     CUI_client = '30197091'
    # elif '5919324' in words_verificare:
    #     CUI_client = '5919324'
    # else:
    #     CUI_client = 'Invalid'

    if not CUI_client:
        CUI_client = 'Invalid'

    def IBAN_furnizor():

        words = []
        position = [[0 for x in range(2)] for y in range(len(text_boxes))]
        boxes_CUI = []

        for i in range(0, len(text_boxes)):
            words.append(text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace('..', ' ').replace(')', ' ').replace('(', ' ').split())
            position[i][0] = text_boxes[i].x_centru
            position[i][1] = text_boxes[i].y_centru

        coordonate_cui = []

        for i in range(len(words)):
            for j in range(len(words[i])):
                if words[i][j].startswith('ro'):
                    # print(words[i][j])
                    boxes_CUI.append(words[i][j])
                    coordonate_cui.append(position[i][0])
                    coordonate_cui.append(position[i][1])
                    break
            if(boxes_CUI):
                break
        
        dict_distante_pozitii = {}
        # print(words)
        try:
            for i in range(0, len(text_boxes)):
                dict_distante_pozitii[math.sqrt(pow((position[i][0] - coordonate_cui[0]), 2) + pow((position[i][1] - coordonate_cui[1]), 2))] = text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace('..', ' ').replace('.', ' ').replace(')', ' ').replace('(', ' ').replace('-', ' ').split()
        except IndexError:
            print("index error line 281")
        sorted_dict = {k: dict_distante_pozitii[k] for k in sorted(dict_distante_pozitii)}
        values = list(sorted_dict.values())

        cui_furnizor = ''

        
        try:
            for i in range(len(values)):
                for j in range(len(values[i])):
                    if values[i][j].startswith('ro') and len(values[i][j])==24 and values[i][j].upper() not in lista_IBAN_client:
                        cui_furnizor = values[i][j].upper()
                        # print(values[i][j])
                        break
                    # INCA UN ELSE IF IN CARE SE VERFICA LUNGIMEA SA FIE DE 24
                    elif values[i][j].startswith('ro') and len(values[i][j])==4 and len(values[i][j+1])==4 and len(values[i][j+2])==4 and len(values[i][j+3])==4 and len(values[i][j+4])==4 and len(values[i][j+5])==4:
                        iban_splitted = []
                        iban_splitted.append(values[i][j])
                        iban_splitted.append(values[i][j+1])
                        iban_splitted.append(values[i][j+2])
                        iban_splitted.append(values[i][j+3])
                        iban_splitted.append(values[i][j+4])
                        iban_splitted.append(values[i][j+5])
                        if ''.join(iban_splitted).upper() not in lista_IBAN_client:
                            cui_furnizor = ''.join(iban_splitted)
                            break

                        # print(cui_furnizor)
                    elif(values[i][j].startswith('ro') and len(values[i][j])==28 and values[i][j][-4:]=='iban'):
                        cui_furnizor = values[i][j][:-4]
                    elif values[i][j].startswith('ro') and len(values[i][j])==4 and len(values[i][j+1])==4 and len(values[i][j+2])==16 and values[i][j].upper() not in [CUI_furnizor, CUI_client]:
                        cui_furnizor = values[i][j] + values[i][j+1] + values[i][j+2]
                    elif not cui_furnizor and values[i][j].startswith('r0') and len(values[i][j])==24 and values[i][j].upper() not in lista_IBAN_client and values[i][j].upper() not in [CUI_furnizor, CUI_client]:
                        cui_furnizor = values[i][j].upper()
                        cui_furnizor = 'RO' + cui_furnizor[2:]
                        break
                        
                    elif not cui_furnizor and values[i][j].startswith('ro') and values[i][j].upper() not in [CUI_furnizor, CUI_client]:
                        try:
                            iban_splitted_test = []
                            iban_splitted_test.append(values[i][j].upper())
                            if len(''.join(iban_splitted_test)) == 24 and ''.join(iban_splitted_test) not in lista_IBAN_client and ''.join(iban_splitted_test)[2:4].isnumeric() and values[i][j].upper() not in [CUI_furnizor, CUI_client] and values[i][j+1].upper() not in [CUI_furnizor[2:], CUI_client[2:]]:
                                cui_furnizor = ''.join(iban_splitted_test)
                                print('test1')
                                break
                            iban_splitted_test.append(values[i][j+1].upper())
                            
                            if len(''.join(iban_splitted_test)) == 24  and ''.join(iban_splitted_test) not in lista_IBAN_client and ''.join(iban_splitted_test)[2:4].isnumeric() and values[i][j].upper() not in [CUI_furnizor, CUI_client] and values[i][j+1].upper() not in [CUI_furnizor[2:], CUI_client[2:]] and '/' not in ''.join(iban_splitted_test):
                                cui_furnizor = ''.join(iban_splitted_test)
                                print('test2')
                                break
                            iban_splitted_test.append(values[i][j+2].upper())

                            if len(''.join(iban_splitted_test)) == 24 and ''.join(iban_splitted_test) not in lista_IBAN_client and ''.join(iban_splitted_test)[2:4].isnumeric() and values[i][j].upper() not in [CUI_furnizor, CUI_client] and values[i][j+1].upper() not in [CUI_furnizor[2:], CUI_client[2:]]:
                                cui_furnizor = ''.join(iban_splitted_test)
                                print('test3')
                                break
                            iban_splitted_test.append(values[i][j+3].upper())
                            if len(''.join(iban_splitted_test)) == 24 and ''.join(iban_splitted_test) not in lista_IBAN_client and ''.join(iban_splitted_test)[2:4].isnumeric() and values[i][j].upper() not in [CUI_furnizor, CUI_client] and values[i][j+1].upper() not in [CUI_furnizor[2:], CUI_client[2:]]:
                                cui_furnizor = ''.join(iban_splitted_test)
                                print('test4')
                                break
                            iban_splitted_test.append(values[i][j+4].upper())
                            if len(''.join(iban_splitted_test)) == 24 and ''.join(iban_splitted_test) not in lista_IBAN_client and ''.join(iban_splitted_test)[2:4].isnumeric() and values[i][j].upper() not in [CUI_furnizor, CUI_client] and values[i][j+1].upper() not in [CUI_furnizor[2:], CUI_client[2:]]:
                                cui_furnizor = ''.join(iban_splitted_test)
                                print('test5')
                                break
                            iban_splitted_test.append(values[i][j+5].upper())
                            if len(''.join(iban_splitted_test)) == 24 and ''.join(iban_splitted_test) not in lista_IBAN_client and ''.join(iban_splitted_test)[2:4].isnumeric() and values[i][j].upper() not in [CUI_furnizor, CUI_client] and values[i][j+1].upper() not in [CUI_furnizor[2:], CUI_client[2:]]:
                                cui_furnizor = ''.join(iban_splitted_test)
                                print('test6')
                                break
                            iban_splitted_test.append(values[i][j+6].upper())
                            
                            if len(''.join(iban_splitted_test)) == 24 and ''.join(iban_splitted_test) not in lista_IBAN_client and ''.join(iban_splitted_test)[2:4].isnumeric() and values[i][j].upper() not in [CUI_furnizor, CUI_client] and values[i][j+1].upper() not in [CUI_furnizor[2:], CUI_client[2:]]:
                                cui_furnizor = ''.join(iban_splitted_test)
                                print(cui_furnizor)
                                break
                        except IndexError:
                            pass
                    elif( values[i][j].startswith('ro') and len(values[i][j])!=24 and len(values[i][j])>20):
                        return 'Invalid'
                    
                if cui_furnizor:
                    break
        except IndexError:
            pass
        if cui_furnizor.upper() in lista_IBAN_client:
            return 'Invalid'
        # print(cui_furnizor)
        return cui_furnizor.upper()
    
    IBAN_furnizor = IBAN_furnizor()

    def IBAN_client():

        words = []
        position = [[0 for x in range(2)] for y in range(len(text_boxes))]
        boxes_CUI = []

        for i in range(0, len(text_boxes)):
            words.append(text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace('..', ' ').replace('.', ' ').replace(')', ' ').replace('(', ' ').split())
            position[i][0] = text_boxes[i].x_centru
            position[i][1] = text_boxes[i].y_centru

        coordonate_cui = []

        for i in range(len(words)):
            for j in range(len(words[i])):
                if words[i][j].startswith('ro'):
                    boxes_CUI.append(words[i][j])
                    coordonate_cui.append(position[i][0])
                    coordonate_cui.append(position[i][1])
                    break
            if(boxes_CUI):
                break

        dict_distante_pozitii = {}

        try:
            for i in range(0, len(text_boxes)):
                dict_distante_pozitii[math.sqrt(pow((position[i][0] - coordonate_cui[0]), 2) + pow((position[i][1] - coordonate_cui[1]), 2))] = text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').replace('..', ' ').replace('.', ' ').replace(')', ' ').replace('(', ' ').split()
        except IndexError:
            print(file)
            print("index error line 521")
        sorted_dict = {k: dict_distante_pozitii[k] for k in sorted(dict_distante_pozitii)}
        values = list(sorted_dict.values())
        test_cui = []
        iban_splitted_test = []
        iban_furnizor1 = IBAN_furnizor
        iban_verifier = iban_furnizor1.lower()
        list_verifier = []
        try:
            list_verifier = [iban_verifier[0:4],iban_verifier[4:8],iban_verifier[8:12],iban_verifier[12:16],iban_verifier[16:20],iban_verifier[20:24] ]
        except Exception:
            pass
        
        try:
            for i in range(len(values)):
                for j in range(len(values[i])):
                    if values[i][j].startswith('ro') and len(values[i][j])==24 and values[i][j]!=iban_verifier and 'furnizor' not in values[i]: 

                        test_cui.append(values[i][j].upper())                 
                    elif(values[i][j].startswith('ro') and len(values[i][j])==4 and values[i][j] not in list_verifier):


                        iban_splitted_test.append(values[i][j].upper())
                        if len(''.join(iban_splitted_test)) == 24:
                            test_cui.append(''.join(iban_splitted_test))
                            break
                        iban_splitted_test.append(values[i][j+1].upper())
                        if len(''.join(iban_splitted_test)) == 24:
                            test_cui.append(''.join(iban_splitted_test))
                            break
                        iban_splitted_test.append(values[i][j+2].upper())
                        if len(''.join(iban_splitted_test)) == 24:
                            test_cui.append(''.join(iban_splitted_test))
                            break
                        iban_splitted_test.append(values[i][j+3].upper())
                        if len(''.join(iban_splitted_test)) == 24:
                            test_cui.append(''.join(iban_splitted_test))
                            break
                        iban_splitted_test.append(values[i][j+4].upper())
                        if len(''.join(iban_splitted_test)) == 24:
                            test_cui.append(''.join(iban_splitted_test))
                            break
                        iban_splitted_test.append(values[i][j+5].upper())
                        if len(''.join(iban_splitted_test)) == 24:
                            test_cui.append(''.join(iban_splitted_test))
                            break
                        iban_splitted_test.append(values[i][j+6].upper())
                        if len(''.join(iban_splitted_test)) == 24:
                            test_cui.append(''.join(iban_splitted_test))
                            break
        except IndexError:
            pass

    
        for i in range(len(values)):
            try:
                if len(values[i]) > 5:
                    for j in range(len(values[i])):
                        concat = values[i][j] + values[i][j+1] + values[i][j+2] + values[i][j+3] + values[i][j+4] + values[i][j+5]
                        if concat.upper() in lista_IBAN_client:

                            return [concat.upper(), concat.upper()]
            except IndexError:
                pass



        try:             
            if len(test_cui[1])>26:
                test_cui[1] = test_cui[1][-24:]
        except IndexError:
            pass

        if(len(test_cui)==1):
            test_cui.append(test_cui[0])


        if len(test_cui) > 1:
            for iban in test_cui:
                if iban not in lista_IBAN_client:
                    test_cui.remove(iban)
            test_cui.append(test_cui[0])

        if not test_cui:
            for i in range(len(values)):
                for j in range(len(values[i])):
                    if values[i][j].upper() in lista_IBAN_client:
                        test_cui.append(values[i][j].upper())
                        test_cui.append(values[i][j].upper())

                        
        return test_cui

    IBAN_client = IBAN_client()

    min_x = text_boxes[0].x_sj
    min_y = text_boxes[0].y_sj

    if search_furnizor(text_boxes[index_box_furnizor].x_sj, text_boxes[index_box_furnizor].x_sj) == None:
        for i in range(1, len(text_boxes)):
            if text_boxes[i].x_sj < min_x and text_boxes[i].y_sj < min_y:
                min_x = text_boxes[i].x_sj
                min_y = text_boxes[i].y_sj

    boxes_serie = []
    for i in range(0, len(text_boxes)):
        for j in range(0, len(lista_factura)):
            if lista_factura[j] in text_boxes[i].text:
                boxes_serie.append(text_boxes[i].text)

    boxes_valoareTotala = []
    for i in range(0, len(text_boxes)):
        for j in range(0, len(lista_total)):
            if lista_total[j] in text_boxes[i].text:
                boxes_valoareTotala.append(text_boxes[i].text)
                try:
                    boxes_valoareTotala.append(text_boxes[i + 1].text)
                except IndexError as e:
                    print(e)

    for i in range(0, len(text_boxes)):
        for j in range(0, len(lista_ron)):
            if lista_ron[j] in text_boxes[i].text:
                boxes_valoareTotala.append(text_boxes[i].text)

    aux = ''
    for i in range(0, len(lista_secundara_furnizor)):
        if lista_secundara_furnizor[i] in factura_client_nume:
            aux = factura_client_nume
            factura_client_nume = factura_furnizor_nume
            factura_furnizor_nume = aux

    '''

    Transforms the final date in "dd/mm/yyy" format

    '''
    def extractDate(x):
        data_final_temp = x.replace('.', '/').replace('-', '/').replace(',', '/')
        if any(c.isalpha() for c in data_final_temp):
            data_final = ''
            for i in range(len(data_final_temp)-1):
                if(data_final_temp[i]==data_final_temp[i+1] == '/'):
                    data_final = data_final_temp[:i] + data_final_temp[i+1:]

            counter_reverse = 0
            for i in reversed(data_final):
                if i=='/' and counter_reverse==2:
                    data_final = data_final[:(len(data_final)-2)] + '20' + data_final[(len(data_final)-2):]
                    break
                counter_reverse+=1

            data_final_temp_1 = data_final_temp.replace('/', ' ').split()
            
            for luna in dictionar_luni.values():
                if(data_final_temp_1[1].startswith(luna)):
                    data_final_temp_1[1] = list(dictionar_luni.keys())[list(dictionar_luni.values()).index(luna)]
            for luna in dictionar_luni_en.values():
                if(data_final_temp_1[1].startswith(luna)):
                    data_final_temp_1[1] = list(dictionar_luni_en.keys())[list(dictionar_luni_en.values()).index(luna)]

            data_final_temp = '/'.join(data_final_temp_1)


        if not data_final_temp[0].isdigit():
            data_final_temp = data_final_temp[1:]


        if not data_final_temp[-1].isdigit():
            data_final_temp = data_final_temp[:-1]

        try: 
            if data_final_temp[0:4].isnumeric():
                x = data_final_temp[-2:]
                y = data_final_temp[0:4]
                data_final_temp = x + data_final_temp[4:8] + y
        except IndexError:
            pass

        if data_final_temp[-3:-2] == '/':
            data_final_temp = data_final_temp[:-2] + '20' + data_final_temp[-2:]
        if data_final_temp[1:2] == '/':
            data_final_temp = '0' +  data_final_temp
        if data_final_temp[2] == '/' and data_final_temp[4] == '/' and data_final_temp[3].isdigit():
            data_final_temp = data_final_temp[:3] + '0' + data_final_temp[3:]

        return data_final_temp


    def numar_factura():

        words = []   
        position = [[0 for x in range(2)] for y in range(len(text_boxes))]
        dates = []
        dict_dates = {}
        vector = []

        for i in range(0, len(text_boxes)):
            words.append(text_boxes[i].text.lower().replace(':', ' ').replace('…', ' ').replace('...', ' ').replace('..', ' ').replace(')', ' ').replace('(', ' ').split())
            position[i][0] = text_boxes[i].x_centru
            position[i][1] = text_boxes[i].y_centru


        date_special_chars = ['/', '-', '.']


        def counter(a):
            counter = 0
            for i in range(len(a)):
                if a[i] in date_special_chars:
                    counter+=1
            return counter

        coordonate_data = []
        
        for k in range(0, len(words)):
            for l in range(0, len(words[k])):
                try:
                    if 'decizia' not in words[k] and CUI_furnizor not in words[k] and parse(words[k][l]) and (len(words[k][l])>=9 or len(words[k][l])==7 or len(words[k][l])==8) and any(c in words[k][l] for c in date_special_chars) and counter(words[k][l])>1 and 'servicii' not in words[k]:
                        dates.append(words[k][l])
                        dict_dates[words[k][l]] = text_boxes[k].y_centru
                except Exception:
                    pass

        # Caz particular reg maria.pdf
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if words[k][l][0:2].isnumeric() and words[k][l][2]==',' and words[k][l+1][0].isdigit() and words[k][l+1][1] == ',' and words[k][l+1][-4:].isnumeric():
                            dates.append(words[k][l].replace(',', '/') + words[k][l+1].replace(',', '/'))
                            dict_dates[words[k][l].replace(',', '/') + words[k][l+1].replace(',', '/')] = text_boxes[k].y_centru
                            coordonate_data.append(position[k][0])
                            coordonate_data.append(position[k][1])
                    except Exception:
                        pass
        # Caz particular F_SRM
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:

                        if words[k][l].isnumeric() and len(words[k][l])==2  and words[k][l+1]=='-' and words[k][l+2].isnumeric() and len(words[k][l+2])==2 and words[k][l+3]=='-' and words[k][l+4].isnumeric() and len(words[k][l+4]) == 4:
                            dates.append(words[k][l] + words[k][l+1] + words[k][l+2] + words[k][l+3] + words[k][l+4])
                            
                            dict_dates[words[k][l] + words[k][l+1] + words[k][l+2] + words[k][l+3] + words[k][l+4]] = text_boxes[k].y_centru
                            coordonate_data.append(position[k][0])
                            coordonate_data.append(position[k][1])
                    except Exception:
                        pass
        #Caz particular FACTURA dr luca catalina
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if len(words[k][l])==1 and words[k][l].isdigit() and words[k+1][0] == '/' and words[k+2][0].isnumeric() and len(words[k+2][0])==2 and len(words[k+3])==2 and words[k+3][0]=='/' and len(words[k+3][1]) == 4:
                            dates.append(words[k][l] + words[k+1][0] + words[k+2][0] + words[k+3][0] + words[k+3][1])
                            dict_dates[words[k][l] + words[k+1][0] + words[k+2][0] + words[k+3][0] + words[k+3][1]] = text_boxes[k].y_centru
                            coordonate_data.append(position[k+1][0])
                            coordonate_data.append(position[k+1][1])
                    except Exception:
                        pass
        # Caz particular aifacturi.ro
        if not dates:
            for i in range(0, len(words)):
                for j in range(0, len(words[i])):
                    try:
                        if words[i][j]=='nr.' and len(words[i])==2 and len(words[i][j+1])==13 :
                            vector.append(words[i][j+1][0:2])
                            vector.append(words[i][j+1][3:].replace('.', '/'))
                            
       
                    except Exception:
                        pass
        # Caz particular factura42
        
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if words[k][l]=='data' and len(words[k][l+1])==5 and len(words[k][l+2])==5 and words[k][l+2][0]=='.':
                            # print('acasd')
                            dates.append(words[k][l+1] + words[k][l+2])
                            dict_dates[words[k][l+1] + words[k][l+2]] = text_boxes[k].y_centru
                            coordonate_data.append(position[k][0])
                            coordonate_data.append(position[k][1])
                    except Exception:
                        pass
         # Caz particular REGINA MARIA  Factura 3.pdf_0
        if not dates:
            # print(words)
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if len(words[k])==2 and len(words[k-1])==3 and words[k-1][-1]=='data' and words[k][0][2]=='.':

                            dates.append(words[k][0] + words[k][1])
                            dict_dates[words[k][0] + words[k][1]] = text_boxes[k].y_centru
                            coordonate_data.append(position[k-1][0])
                            coordonate_data.append(position[k-1][1])
                    
                    except Exception:
                        pass

        #Caz particular factura45.2020.pdf_0
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if 'decizia' not in words[k] and parse(words[k][l]) and (len(words[k][l])>=9 or len(words[k][l])==7 or len(words[k][l])==8) and any(c in words[k][l] for c in date_special_chars) and counter(words[k][l])>1 and 'servicii' not in words[k]:
                            dates.append(words[k][l])
                            dict_dates[words[k][l]] = text_boxes[k].y_centru
                    except Exception:
                        pass
        
        # Caz particular FACTURA 2021001_MATERNA CARE_Regina Maria_250 LEI.pdf_0
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if words[k][l][0].isdigit() and words[k][l][-1].isdigit() and words[k][l][1].isdigit() and words[k][l][3:6] in ["ian", "feb", "mar", "apr", "mai", "iun", "iul", "aug", "sep", "oct", "nov","noi", "dec"]:
                            dates.append(words[k][l])
                            dict_dates[words[k][l]] = text_boxes[k].y_centru
                    except Exception:
                        pass


        #Caz particular Regina nov 2020.pdf_0
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if parse(words[k][l]) and len(words[k][l])>7 and len(words[k][l])<10:
                            dates.append(words[k][l])
                            dict_dates[words[k][l]] = text_boxes[k].y_centru
                    except Exception:
                        pass
        # print('s', dates)
        if not dates:
            #Caz particular ANI0022 Factura Regina Maria noi 2020
            if words[0] == ['factura'] and words[1] == ['no.', 'date'] and len(words[2]) == 3 and words[2][2].isnumeric() and len(words[3])==3 and  words[3][1].isalpha():
                temp = words[3]
                for luna in dictionar_luni.values():
                    if(temp[1].startswith(luna)):
                        temp[1] = list(dictionar_luni.keys())[list(dictionar_luni.values()).index(luna)]
                vector.append(words[2][2])
                vector.append('/'.join(temp))

        # CENTRUL MED UNIREA 
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if words[k][l][-4:].isnumeric() and words[k][l][-5] == ',' and words[k][l][2] == ',' and len(words[k][l]) == 10 and words[k][l][1].isdigit() and words[k][l][4].isdigit():
                            dates.append(words[k][l])
                            dict_dates[words[k][l]] = text_boxes[k].y_centru
                    except Exception:
                        pass
        # facturi CIP (1)
        # print(words)
        if not dates:
            try:
                if words[1] == ['factura'] and len(words[2]) == 10 and words[2][5] == 'zi/luna/an' and words[2][2] == 'nr.' and words[2][3].isdigit() and words[2][-4].isdigit() and words[2][-3] == '/' and len(words[2][-4] + words[2][-3] + words[2][-2] + words[2][-1])==10:
                    # print('sss')
                    try:
                        vector.append(words[2][3])
                        vector.append(words[2][-4] + words[2][-3] + words[2][-2] + words[2][-1])
                    except Exception:
                        pass
            except IndexError:
                pass
        # print(words)
        if not dates:
            if words[0] == ['factura'] and words[1] == ['seria'] and words[2] == [] and words[4] == [] and len(words[5])==3 and len(words[6]) == 2 and words[6][0] == 'data' and words[5][0] == 'nr.' and  words[5][1] == 'facturii'  and  words[5][2].isdigit() and '.' in words[6][1]:
                try:
                   vector.append(words[5][2])
                   if words[6][1][1] == '.' and words[6][1][-5:].isnumeric():
                        vector.append('0' + words[6][1].replace('.', '/')[:-2] + words[6][1][-1])
                except Exception:
                    pass 
        # print(words)
        # Factura Decembrie 2020_Mihaela Anghel
        if not dates:
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    try:
                        if words[k][l].isdigit() and words[k][l+2].isnumeric() and parse(words[k][l] + words[k][l+1] + words[k][l+2]):
                            for luna in dictionar_luni_en.values():
                                if(words[k][l+1].startswith(luna)):
                                    dates.append(words[k][l] + '/' + words[k][l+1] + '/' + words[k][l+2])
                                    dict_dates[words[k][l]] = text_boxes[k].y_centru
                    except Exception:
                        pass

        try:
            for i in range(len(dates)):
                if not dates[i][-1].isdigit():
                    dates[i] = dates[i][:-1]

            new_dict = {}
            for key, value in dict_dates.items():
                if not key[-1].isdigit():
                    new_dict[key[:-1]] = value
                    
                else:
                    new_dict[key] = value
            dict_dates = new_dict
 
            data_min = min(dates)

            '''
            Se scot din dates toate datile care nu respecta: 25 luna trecuta < data < today
            '''
            new_dates = []
            # print('da')
    
            for d in dates:
                #data din factura
                a = extractDate(d)
                #data din factura extrasa
                try:
                    date_time_obj = datetime.strptime(a, '%d/%m/%Y')
                except ValueError:
                    pass

                # azi
                today = date.today()
                tempDate = datetime.utcnow().replace(day=1) - timedelta(days=1) 
                # 25 luna trecuta
                lastDate = tempDate.replace(day=25)
                # print(date_time_obj)
                try:
                    if lastDate.date() <= date_time_obj.date() <= today:
                        new_dates.append(d)
                except Exception:
                    print('Exception -> line 1004')

            dictionary_helper = {}
            for dat in new_dates:
                a = extractDate(dat)
                try:
                    date_time_obj = datetime.strptime(a, '%d/%m/%Y')
                except ValueError:
                    pass
                dictionary_helper[dat] = date_time_obj.date()


            try:
                data_min = min(dictionary_helper, key=dictionary_helper.get)
            except ValueError:
                pass
            
            try:
                if not data_min:
                    data_min = dates[0]
            except IndexError:
                pass


            '''
             INVOICE NUMBER CALCULATION
            '''
            for k in range(0, len(words)):
                for l in range(0, len(words[k])):
                    if words[k][l] == data_min:
                        
                        coordonate_data.append(position[k][0])
                        coordonate_data.append(position[k][1])


            # Factura Decembrie 2020_Mihaela Anghel
            if not coordonate_data:
                for k in range(0, len(words)):
                    for l in range(0, len(words[k])):
                        try:
                            if words[k][l] + words[k][l+1] + words[k][l+2] == data_min.replace('/', ''):
                                coordonate_data.append(position[k][0])
                                coordonate_data.append(position[k][1]) 
                        except Exception:
                            pass

            dict_distante_pozitii = {}
            try:
                for i in range(0, len(text_boxes)):
                    dict_distante_pozitii[math.sqrt(pow((position[i][0] - coordonate_data[0]), 2) + pow((position[i][1] - coordonate_data[1]), 2))] = text_boxes[i].text.lower().replace('…', ' ').replace('...', ' ').replace('..', ' ').replace('nr.', ' ').replace('_', ' ').replace(':', ' ').replace('a-', ' ').split()
            except IndexError:
                pass
            sorted_dict = {k: dict_distante_pozitii[k] for k in sorted(dict_distante_pozitii)}
            
            values = list(sorted_dict.values())
            # print(values)
            nr_factura = ""

            checker_list  = [CUI_client.lower(), CUI_furnizor.lower()]
            #caz particular factura_2020-5_2020-12-03.pdf_0
            try:
                if not nr_factura:
                    if len(values[0])==2 and values[0][1] == data_min and '-' in values[0][0] and factura_furnizor_nume.startswith('Mateescu'):
                        nr_factura = values[0][0].replace('-', ' ').split()[1]
                        # print(data_min)
            except IndexError:
                pass

            #caz particular Fact 121-04.12.2020.pdf_0
            try:
                if not nr_factura:
                    if len(values[0])==69 and values[0][-3:]== ['cota', 'tva', '0%'] and values[0][:4]==['furnizor', 'dsd', 'denta', 'med'] and values[0][-8] =='seria':
                        nr_factura = values[0][-6]
            except IndexError:
                pass
                    
            # caz particular Regina nov 2020.pdf_0
            if not nr_factura:
                try: 
                    if values[0] == [data_min] and values[4] == ['pret', 'unitar', 'fara', 'tva'] and values[9][0].isnumeric():
                        nr_factura = values[9][0]
                except IndexError:
                    pass
            # caz particular Factura_PI41.pdf_0
            if not nr_factura:
                try:
                    if values[0] == ['dată', 'facturare',data_min] and values[2] == ['factura'] and len(values[3])==2 and values[3][0] == 'număr' and '-' in values[3][1]:
                        nr_factura = values[3][1].replace('-', ' ').split()[1]
                except IndexError:
                    pass
            
            # caz particular Factura_MVL0050.pdf_0
            if not nr_factura:
                try:
                    if values[0] == ['dată', 'facturare',data_min] and values[4] == ['factura'] and len(values[3])==2 and values[3][0] == 'număr' and values[3][1][-1].isdigit():
                        nr_factura = re.split('(\d+)',values[3][1])[1]
                except IndexError:
                    pass
            
            # Factura_Gin-1_09.01.2021
            if not nr_factura:
                try:
                    if values[0][0].replace('-', ' ').split()[1].isdigit() and len(values[0]) ==2 and values[0][1][-2:] == data_min[-2:] and values[1][:11]==['factură', 'seria', 'și', 'numărul', 'facturii', 'data', 'facturii', '(zi.luna.an)', 'termen', 'de', 'plată']:

                        nr_factura = values[0][0].replace('-', ' ').split()[1]
                except IndexError:
                    pass

            # Factura DA2020005FC din 07_01_2021
            if not nr_factura:
                try:
                    if values[0][0] == data_min and len(values[0]) == 1 and values[1][0] == 'factura' and values[1][2:] == ['data', '(ziua,', 'luna,', 'anul)'] and values[2][0] == 'factura' and values[3] == ['cod', 'client', 'c.i.f.', 'r.c.', 'banca']:
                        val = re.sub('\D', '', values[1][1])
                        if val.isdigit():
                            nr_factura = val
                except IndexError:
                    pass

            # Factura Decembrie 2020_Mihaela Anghel
            if not nr_factura:
                try:
                    for luna in dictionar_luni_en.values():
                        if(data_min.replace('/', ' ').split()[1].startswith(luna)):
                            if not nr_factura:
                                for i in range(len(values)):
                                    for j in range(len(values[i])):
                                        try:
                                            if values[i][j-1] not in luni_helper and values[i][j]!='0' and not nr_factura and not (len(values[i])==3 and values[i][-1] == 'lei') and values[i][j-1] not in ['sector', 'balaseanu'] and values[i][j].isnumeric() and values[i][j] not in checker_list  or ( values[i][j][:2]!='ro' and  values[i][j][-1].isdigit() and values[i][j][0].isalpha() and values[i][j].isalnum()) and values[i][j-1] not in ['seria', 'serie']: # AICI avea si and len(values[i][j])>1
                                                try:
                                                    if not nr_factura and values[i][j] not in data_min.replace('/', ' ').split():
                                                        nr_factura = values[i][j]
                                                        break
                                                except Exception:
                                                    pass
                                        except IndexError:
                                            pass
                                    if nr_factura:
                                        break
                except Exception:
                    pass

            # fact_0098.pdf_0
            if not nr_factura:
                try:
                    if values[0][1] == data_min and len(values[0]) == 2 and values[0][0].startswith('numar-') and values[1][0] == 'serie':
                        if values[0][0].replace('-', ' ').split()[1].isdigit():
                            nr_factura = values[0][0].replace('-', ' ').split()[1]
                except IndexError:
                    pass

            # Factura nr 65dec2020- Regina Maria
            if not nr_factura:
                try:
                    if values[0][2] == data_min and len(values[0]) == 3 and values[5] == ['seria', 'numar', 'data'] and values[6] ==['cantitate'] and values[0][1].isdigit() and values[0][0][-1].isdigit() and values[0][0][0].isalpha() and not values[1] and not values[2] and not values[3] and not values[4] and values[8] == ['fiscala']:
                        nr_factura = values[0][1]
                except IndexError:
                    pass

            '''
            Applied for Ibans(xxxx xxxx xxxx ...)
            values[i][j-1] not in ibans_splitted and values[i][j+1] not in ibans_splitted
            '''    
            ibans_concat = ''
            for iban_cl in IBAN_client:
                ibans_concat += iban_cl
            ibans_concat += IBAN_furnizor

            ibans_splitted = [ibans_concat[i:i+4] for i in range(0, len(ibans_concat), 4)]


            if not nr_factura:
                for i in range(len(values)):
                    for j in range(len(values[i])):
                        try:
                            if values[i][j-1] not in ['ap','sector', 'sc'] and values[i][j-1] not in luni_helper and values[i][j]!='0' and not nr_factura and not (len(values[i])==3 and values[i][-1] == 'lei') and values[i][j-1] not in ['sector', 'balaseanu'] and values[i][j].isnumeric() and values[i][j] not in checker_list  or ( values[i][j][:2]!='ro' and  values[i][j][-1].isdigit() and values[i][j][0].isalpha() and values[i][j].isalnum()) and values[i][j-1] not in ['seria', 'serie']: # AICI avea si and len(values[i][j])>1

                                try:
                                    # Factura_E0029
                                    if values[i+1] == ['factura'] and len(values[i+2]) == 2 and values[i+2][0] == 'număr' and values[i+2][1][-1].isdigit() and values[i+3] == ['preț', 'unitar'] and values[i+4] == ['-ron-']:
                                        print('s')
                                        nr_factura = values[i+2][1]
                                        break
                                except Exception:
                                    pass
                                try:
                                    if values[i][j-1] == 'serie' and values[i][j+1] == 'numar' and values[i][j+2].isdigit() and values[i][j+2]!='0':
                                        nr_factura = values[i][j+2]
                                except Exception:
                                    pass
                                if len(values[i])>3:
                                    if values[i][j-1] not in ibans_splitted and values[i][j+1] not in ibans_splitted:
                                        if not nr_factura:
                                            nr_factura = values[i][j]
                                            break
                                else:
                                    if not nr_factura:
                                        nr_factura = values[i][j]
                                        break
                        except IndexError:
                            pass
                    if nr_factura:
                        break
                        
            
            try:
                if nr_factura[-1].isdigit() and nr_factura[0].isalpha():
                    nr_factura = re.split('(\d+)',nr_factura)[1]
            except IndexError:
                pass


            if not vector:
                vector.append(nr_factura)
                
                vector.append(extractDate(data_min))

            # print(vector)
            return vector
        except ValueError:
            pass
        # Caz particular aifacturi.ro

        if vector:
            return vector

    def total():

        words = []
        position = [[0 for x in range(2)] for y in range(len(text_boxes))]
        boxes_CUI = []

        for i in range(0, len(text_boxes)):
            words.append(text_boxes[i].text.lower().replace(':', ' ').replace(',', ' ').split())
            position[i][0] = text_boxes[i].x_sj
            position[i][1] = text_boxes[i].y_sj

        coordonate_cui = []

        for i in range(len(lista_total)):
            for j in range(len(words)):
                for k in range(len(words[j])):
                    if words[j][k] == lista_total[i]:
                        boxes_CUI.append(words[j][k])
                        coordonate_cui.append(position[j][0])
                        coordonate_cui.append(position[j][1])
                        # print(words[j][k], coordonate_cui, 'cucu')

                        break
                if(boxes_CUI):
                    break
        
        # print(coordonate_cui)

        dict_distante_pozitii = {}
        # for i in range(0, len(text_boxes)):
        #     print(text_boxes[i].text) 
        b = []
        '''
        random.uniform(0.0000000000000, 0.0000001) added to avoid duplicate keys in dictionary
        '''
        try:
            for i in range(0, len(text_boxes)):

                dict_distante_pozitii[math.sqrt(0 + pow((position[i][1] - coordonate_cui[1]), 2)) ] = text_boxes[i].text.lower().replace(':', ' ').split()
        except IndexError:
            print(file)
            print("index error line 787")

        sorted_dict = {k: dict_distante_pozitii[k] for k in sorted(dict_distante_pozitii)}
        values = list(sorted_dict.values())
        # print('MACARAOANE',dict_distante_pozitii)
        # print('SUC',sorted_dict)
        test_cui = []

        for i in range(len(values)):
            for j in range(len(values[i])):
                if values[i][j][0].isnumeric():
                    test_cui.append(values[i][j])

        def dotcounter(a):
            counter = 0
            for i in range(len(a)):
                if a[i] == '.':
                    counter+=1
            return counter
        cui_furnizor = ''
        # print(values)
        # caz particular Fact 121-04.12.2020.pdf_0
        try:
            if len(values[0]) == 37 and values[0][0] == '1.' and values[0][6] == values[0][7] and values[0][5].isdigit() and values[0][8].isdigit():
                cui_furnizor = values[0][6]
        except IndexError:
            pass

        temp_join = []


        # Factura Decembrie 2020_Mihaela Anghel
        if not cui_furnizor and ['nr', 'crt', 'descriere'] in values:

            try:
                for i in range(len(values)):
                    for j in range(len(values[i])):
                        
                        if 'euro' != values[i][j-1] and 'lei/eur;' not in values[i] and not cui_furnizor and values[i][j][0].isnumeric() and '/' not in values[i][j] and not any(c.isalpha() for c in values[i][j]) and (dotcounter(values[i][j])<2 and dotcounter(values[i][j])>0 or ',' in values[i][j]) and values[i][j][-1]!=',' and values[i][j][-1]!='.' and values[i][j]!='1,00':
                        
                            if values[i][j][0] != '0' and values[i+1] == ['nr', 'crt', 'descriere']:
                                cui_furnizor = values[i][j]
                                break

                    if cui_furnizor:
                        break
            except IndexError:
                pass

        
        if not cui_furnizor:
            try:
                for i in range(len(values)):
                    for j in range(len(values[i])):
                        
                        # caz particular factura44.2020.pdf_0
                        if values[i] == ['total', '(lei)', 'din', 'care', 'accize'] and len(values[i+1])==1 and values[i+1][0][0].isdigit() and values[i+2] == ['total', 'de', 'plata']:
                            cui_furnizor = values[i+1][0]
                            break
                        # caz particular GHE 100.pdf_0
                        if not cui_furnizor and len(values[i])==1 and values[i][0].isnumeric() and len(values[i+1])==2 and values[i+1][0].isalpha() and values[i+1][1].isalpha() and len(values[i+2])==2 and values[i+2][0].isalpha() and values[i+2][1].isalpha():
                            cui_furnizor = values[i][0]
                            break
                        if 'euro' != values[i][j-1] and 'lei/eur;' not in values[i] and not cui_furnizor and values[i][j][0].isnumeric() and '/' not in values[i][j] and not any(c.isalpha() for c in values[i][j]) and (dotcounter(values[i][j])<2 and dotcounter(values[i][j])>0 or ',' in values[i][j]) and values[i][j][-1]!=',' and values[i][j][-1]!='.' and values[i][j]!='1,00':

                            # if for Factura Regina Maria septembrie 2020-converted.pdf_0
                            if len(values[i])==6 and len(values[i+1])==2 and values[i][1] == values[i+1][0] and ',' in values[i][1] and len(values[i+2]) == 0:
                                cui_furnizor = values[i][1]
                                break
                            # if for FacturaREG0010-CENTRUL_MEDICAL_UNIREA_SRL.pdf_0
                            if len(values[i])==3 and len(values[i+1])==0 and values[i][2] == 'ron' and values[i][0] == values[i+2][0]:
                                cui_furnizor = values[i][1]
                                break
                            if values[i][j-1].isnumeric() :
                                temp_join.append(values[i][j-1])
                                temp_join.append(values[i][j])
                                cui_furnizor = ''.join(temp_join)
                                # print('abubaca')
                                break
                            if values[i][j][0] != '0':
                                cui_furnizor = values[i][j]
                                break

                    if cui_furnizor:
                        break
            except IndexError:
                pass
        # print(cui_furnizor)
        if not cui_furnizor:
            a = []
            for i in range(0, len(text_boxes)):
                a.append(text_boxes[i].text.lower().replace(':', ' ').split())
            for i in range(0, len(a)):
                for j in range(0, len(a[i])):
                    # print(a[i])
                    if a[i][j][0].isnumeric() and '/' not in a[i][j] and not any(c.isalpha() for c in a[i][j]) and (dotcounter(a[i][j])<2 and dotcounter(a[i][j])>0 or ',' in a[i][j]) and a[i][j][0] != '0' and a[i][j][-1]!=',' and a[i][j][-1]!='.':
                        if len(a[i]) == 2 and a[i][0].isnumeric():
                            cui_furnizor = a[i][0] +  a[i][1]
                        else:
                            cui_furnizor = a[i][j]
                        # print(a[i][j], 'spec')

        if not cui_furnizor:
            try:
                for i in range(len(values)):
                    for j in range(len(values[i])):
                        if 'servicii' not in values[i] and  len(values[i][j])>2 and values[i][j][0].isnumeric() and '/' not in values[i][j] and not any(c.isalpha() for c in values[i][j])  and values[i][j][-1]!=',' and values[i][j][-1]!='.' and values[i][j][0] != '0':
                            cui_furnizor = values[i][j]
                            break
                    if cui_furnizor:
                        break
            except IndexError:
                pass
        
        
        total = ''
        # print(cui_furnizor)
        if(cui_furnizor.isnumeric()):
            return cui_furnizor + '.00'
        
        elif cui_furnizor:

            if cui_furnizor[-2:-1]=='.':
                cui_furnizor +=  '0'
            # if cui_furnizor[-3:].isnumeric() and cui_furnizor[-1] == '0':       MARE GRIIJA CA AI DECOMENTAT ASTA PENTRU DR.CImpeanu 
            #     cui_furnizor = cui_furnizor[:-1]

            a = cui_furnizor.replace(',', ' ').replace('.', ' ').split()
            # print(a)
            if cui_furnizor[-3:].isnumeric() and len(a[0]) <3 and len(a)==2:
                cui_furnizor += '00'

            # print(cui_furnizor)

            b = cui_furnizor.replace(',', ' ').split()

            if len(b) ==2 and len(b[1])==1:
                cui_furnizor += '0'

            total_temp = cui_furnizor.replace(',', '').replace('.', '')

            if len(total_temp) < 6:
                total = total_temp[-5:-2] + '.' + total_temp[-2:]
            elif len(total_temp) > 5:
                total = total_temp[:-5] + ',' + total_temp[-5:-2] + '.' + total_temp[-2:]
                
        # print(total)

        # print(values)
        total_f = total.replace(',', '')

        try:
            if total_f[0] == '0':
                total_f = total_f[1:]
            if total_f[0] == '00':
                total_f = total_f[2:]
        except IndexError:
            pass

        return total_f



        
    vector = numar_factura()
                
    try:
        numar_factura = vector[0]
        data_factura = vector[1]
    except TypeError:
        numar_factura = "Null"
        data_factura = "Null"
    if numar_factura is None:
        numar_factura = "Null"


    cui_f = CUI_furnizor
    cui_c = CUI_client

    if cui_f  in lista_CUI_client:
        cui_f = CUI_client
        cui_c = CUI_furnizor

    IBAN_f = IBAN_furnizor
    try:
        IBAN_c = IBAN_client[1]
    except IndexError:
        IBAN_c = 'Invalid'

    if IBAN_f in lista_IBAN_client:
        try:
            IBAN_f = IBAN_client[1]
        except IndexError:
            IBAN_f = 'Invalid'
        IBAN_c = IBAN_furnizor

    if not IBAN_client:
        IBAN_c = 'Invalid'
    
    if IBAN_f == IBAN_c:
        IBAN_f = 'Invalid'

    if not IBAN_f:
        IBAN_f = 'Invalid'

    if not cui_f:
        cui_f = 'Invalid'

    if not cui_c:
        cui_c = 'Invalid'

    if IBAN_f == "RO14INGB0000999905816003":
            cui_f = "33610285"
    if IBAN_f == "RO37INGB0000999908159594":
            cui_f = "38095660"
    if cui_f =="075100":
        cui_f="30911445"

    factura ={"Furnizor": {
            "Nume": factura_furnizor_nume,
            "cod": cui_f,
            "IBAN": IBAN_f,

        },
            "Client": {
                "Nume": factura_client_nume,
                "cod": cui_c,
                "IBAN": IBAN_c,

            },
            "total": total(),
            "numar_factura": numar_factura,
            "data": data_factura, 
            "nume_factura": file
        }
    print(factura)
   
    
    # Serializing json
    json_object = json.dumps(factura, indent=4)

    # Writing to sample.json
    nume_fisier = f'{numar}'
    if numar_factura in file or numar_factura.startswith('00'):
        nume_fisier = nume_fisier+'_VERIFICAT'
    json_dir = "C:\\Users\\quasar\\invoice_handling\\"+folder+"\\3.0_INVOICE_JSON\\" #"C:\\Users\\quasar\\invoice_handling\\2021\\februarie\\test\\3.0_INVOICE_JSON\\"
    with open(json_dir + nume_fisier + ".json", "w") as outfile:
        outfile.write(json_object)

procesate = "C:\\Users\\quasar\\invoice_handling\\"+folder+"\\2.1_procesate\\" #"C:\\Users\\quasar\\invoice_handling\\"+folder+"

numar = 1
dir = "C:\\Users\\quasar\\invoice_handling\\"+folder+"\\2.0_PDF_FILES_splited\\"
for file in os.listdir(dir):
    if file.endswith('.pdf') or file.endswith('.PDF'):
        fp = open(dir + file, 'rb')
        try:
            main(fp, numar, file)
        except TypeError:
            print('Type error')

        # try:
        #     os.rename(dir + file, procesate + today +'_'+ file)
        # except FileExistsError:
        #     os.remove(dir + file)
        #     print("============= Fisier parsat deja =============")

        numar = numar + 1
        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------')
