import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import shutil
import datetime

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
# folder = str(folder_an) + "\\" + nume_luna + "\\test4"


#!!!!!!!!!!!!!!!!!!!!! decomenteaza ultima linie care muta fisierele
input_dir = 'C:\\Users\\quasar\\invoice_handling\\'+folder+'\\1.0_EMAIL_DUMP\\'
procesate = 'C:\\Users\\quasar\\invoice_handling\\'+folder+'\\1.1_procesate\\'
output_dir = 'C:\\Users\\quasar\\invoice_handling\\'+folder+'\\2.0_PDF_FILES_splited\\'

#  = 'C:\\Users\\quasar\\invoice_handling\\Noiembrie\\1.0_EMAIL_DUMP\\'
# input_dir = 'C:\\Users\\quasar\\invoice_handling\\Noiembrie\\1.1_procesate\\'
# output_dir = 'C:\\Users\\quasar\\invoice_handling\\Noiembrie\\pdf_splited_erori_plm\\'


files_to_move = []
existing_files=[]
count=0
for file in os.listdir(procesate):
    existing_files.append(file)
    count=count+1
print(existing_files)
print(count)
for file in os.listdir(input_dir):
    # pdf_file = open(input_dir + file, "rb")
    # inputpdf = PdfFileReader(pdf_file, strict = False)
    print(file)
    if file in existing_files:
        print("""
            
            EXISTA DEJA=================================================================================================================================================================

        """)
        # os.remove(input_dir+file)
    else:   
        with open(input_dir + file, "rb") as f:
            try:
                
                inputpdf = PdfFileReader(f, strict = False)
                #with open(input_dir + file, "rb") as f:
                #f=open(input_dir + file, "rb")
                #inputpdf = PdfFileReader(f, "rb")
                
            except TypeError as e:
                print(e)
                files_to_move.append(file)
                pass
            except Exception as e:
                print(e)
                files_to_move.append(file)
                pass

            try:
                if inputpdf.isEncrypted:
                    inputpdf.decrypt('')
                for i in range(0, inputpdf.numPages):
                    output = PdfFileWriter()
                    output.addPage(inputpdf.getPage(i))

                    with open(output_dir + file[:-4] + "_%s.pdf" % i, "wb") as outputStream:
                        output.write(outputStream)
            except NotImplementedError:
                pass
            except TypeError:
                pass
        try:
            os.rename(input_dir+file, procesate+file)
        except FileExistsError:
            pass
    


    #----------------------------------------------------------------
# for file in os.listdir(input_dir):
#     try:
#         os.rename(input_dir+file, procesate+file)
#     except FileExistsError:
#         os.remove(input_dir+file)
#         pass

# for j in range(0, len(files_to_move)):
#     try:
#         os.rename(input_dir + files_to_move[j], 'C:\\Users\\quasar\\invoice_handling\\Noiembrie\\1.2_Unreadable_PDF\\' + files_to_move[j])
#     except FileExistsError:
#         pass
#     except FileNotFoundError:
#         pass


# import fitz

# def extractText(file): 
#     doc = fitz.open(file) 
#     text = []
#     for page in doc: 
#         t = page.getText().encode("utf8") 
#         text.append(t)
#     return text



    