import fitz
import PyPDF2 
import site
import sys
site.addsitedir("../../../PDFNetC/Lib")
import sys
import site
site.addsitedir("../../../PDFNetC/Lib")
import sys
from PDFNetPython3 import *
import os
from datetime import *
import time

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
folder = str(folder_an) + "\\" + nume_luna + "\\" + str(folder_zi)+"\\"
folder_rapoarte = str(folder_an) + "\\" + nume_luna + "\\" + "auxiliar\\"

reports = 'C:\\Users\\quasar\\rapoarte\\'+folder_rapoarte
folder_grupuri = 'C:\\Users\\quasar\\rapoarte\\'+folder
invoices = 'C:\\Users\\quasar\\invoice_handling\\'+folder+"2.0_PDF_FILES_splited\\"


#########################################################################
############################## MERGE PDF ################################
#########################################################################
for file in os.listdir(reports):

    nume_factura = file[file.index("_#3#_")+5:-4]
    print(nume_factura)
    # Open the files that have to be merged one by one
    pdf2File = open(reports+file, 'rb')
    pdf1File = open(invoices+nume_factura, 'rb')
    # pdf2File = open(invoices+file.split("##")[0]+".pdf", 'rb')
    
    # Read the files that you have opened
    pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
    pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
    
    # Create a new PdfFileWriter object which represents a blank PDF document
    pdfWriter = PyPDF2.PdfFileWriter()
    
    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    
    # Loop through all the pagenumbers for the second document
    for pageNum in range(pdf2Reader.numPages):
        pageObj = pdf2Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    
    # Now that you have copied all the pages in both the documents, write them into the a new document
    pdfOutputFile = open('C:\\Users\\quasar\\rapoarte\\'+folder+file[:file.index("_#3#_")]+'.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)
    
    # Close all the files - Created as well as opened
    pdfOutputFile.close()
    pdf1File.close()
    pdf2File.close()

    #########################################################################
    ############################ APPLY IMAGE ################################
    #########################################################################

    input_file = 'C:\\Users\\quasar\\rapoarte\\'+folder+file[:file.index("_#3#_")]+'.pdf'
    output_file = 'C:\\Users\\quasar\\rapoarte\\'+folder+file[:file.index("_#3#_")]+'_watermark'+'.pdf'
    barcode_file = "C:\\Users\\quasar\\rapoarte\\stampila_upside_down.png"
    barcode_file_factura = "C:\\Users\\quasar\\rapoarte\\stampila_normala.png"

    # define the position (upper-right corner)
    image_rectangle = fitz.Rect(800,300,950,700)
    image_rectangle_factura = fitz.Rect(200,600,380,750)
    print(image_rectangle)
    # retrieve the first page of the PDF
    file_handle = fitz.open(input_file)
    # first_page = file_handle[0]
    # first_page._cleanContents()

    # add the image
    for i in range(0,len(file_handle)):
        print(file_handle)
        if i==0:
            page = file_handle[i]
            page.insertImage(image_rectangle_factura, filename=barcode_file_factura)
        page = file_handle[i]
        page.insertImage(image_rectangle, filename=barcode_file)

    file_handle.save(output_file)


#########################################################################
################ Delete PDFs without watermark ##########################
#########################################################################

for file in os.listdir(folder_grupuri):
    print('in for')
    if "_watermark" not in file:
        print('in if')
        with open(folder_grupuri+file) as f:
            print("in with")
            pass 
        try:
            os.remove(folder_grupuri+file)
        except PermissionError as e:
            print(e)
        # try:
        #     os.remove(folder_grupuri+file)
        # except PermissionError as e:
        #     print(e,'al doilea')

#########################################################################
########################### COMPRESS PDF ################################
#########################################################################


PDFNet.Initialize()
for file in os.listdir(folder_grupuri):
    doc = PDFDoc('C:\\Users\\quasar\\rapoarte\\'+folder+file)
    doc.InitSecurityHandler()
    Optimizer.Optimize(doc)
    file_save = file[:-4]
    doc.Save('C:\\Users\\quasar\\rapoarte\\'+folder+file_save+'_optim_'+'.pdf', SDFDoc.e_linearized)
    doc.Close()

for file in os.listdir(folder_grupuri):
    print('in for')
    if "_watermark" not in file:
        print('in if')
        with open(folder_grupuri+file) as f:
            print("in with")
            pass 
        try:
            os.remove(folder_grupuri+file)
        except PermissionError as e:
            print(e)

for file in os.listdir(folder_grupuri):
    if '_optim' in file:
        grup = file[file.index('_#2#_')+5:file.index('_watermark_optim')]
        print(grup)
        try:
            os.mkdir(folder_grupuri+grup)
        except FileExistsError:
            pass
        final_file = file.replace('_#2#_'+grup+'_watermark_optim_','')
        final_file = final_file.replace('_#1#_','_____HR____')
        os.rename(folder_grupuri+file,folder_grupuri+grup+'\\'+final_file)

time.sleep(5)
for file in os.listdir(folder_grupuri):
    if file.endswith('.pdf'):
        folder_grupuri_minus_grup = folder_grupuri.replace(grup,'')
        print(folder_grupuri)
        print(file)
        try:
            os.remove(folder_grupuri_minus_grup+file)
        except PermissionError:
            try:
                os.remove(folder_grupuri_minus_grup+file)
            except PermissionError as e:
                print(e)