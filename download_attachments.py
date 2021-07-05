import imaplib
import email
import os
import imap_tools
import base64
import csv
import datetime
from datetime import date, timedelta
import random

lista_cuvinte_de_nedownloadat = ["malpraxis", "proforma", "polita", "constitutiv", "anexa", "ci", "aviz"]

now = datetime.datetime.now()
yesterday = date.today() + timedelta(days=-1)

zi_download = yesterday.strftime('%d')
zi_pana_cand_download = date.today().strftime('%d')

luna_download = yesterday.strftime('%m')
luna_pana_cand_download = date.today().strftime('%m')

dict_luna_nr_nume = {
  "01": "Jan",
  "02": "Feb",
  "03": "Mar",
  "04": "Apr",
  "05": "May",
  "06": "Jun",
  "07": "Jul",
  "08": "Aug",
  "09": "Sep",
  "10": "Oct",
  "11": "Nov",
  "12": "Dec"
}

luna_download = dict_luna_nr_nume[luna_download]
luna_pana_cand_download = dict_luna_nr_nume[luna_pana_cand_download]

an_download = yesterday.strftime('%y')
an_pana_cand_download = date.today().strftime('%y')

mail_search_de_cand = '"' + zi_download + '-' + luna_download + '-' + "20" + an_download + '"'
mail_search_pana_cand = '"' + zi_pana_cand_download + '-' + luna_pana_cand_download + '-' + "20" + an_pana_cand_download + '"'

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

outputdir = 'C:\\Users\\quasar\\invoice_handling\\'+folder
rapoarte = 'C:\\Users\\quasar\\rapoarte\\'+folder
try:
    os.makedirs(outputdir)
except FileExistsError:
    pass

try:
    os.mkdir(outputdir+"\\1.0_EMAIL_DUMP")
    os.mkdir(outputdir+"\\1.1_procesate")
    os.mkdir(outputdir+"\\2.0_PDF_FILES_splited")
    os.mkdir(outputdir+"\\2.1_procesate")
    os.mkdir(outputdir+"\\3.0_INVOICE_JSON")
    os.mkdir(outputdir+"\\3.1_procesate")
    os.mkdir(outputdir+"\\4_VALIDATE_ERROR")
    os.mkdir(outputdir+"\\5_VALIDATE_INVOICE")
    os.mkdir(outputdir+"\\6_FILL_PLM")
    os.mkdir(outputdir+"\\7_FILL_PLM_ERROR")
    os.mkdir(outputdir+"\\8_FILL_PLM_Introduse")
    os.mkdir(outputdir+"\\9_FILL_PLM_Existente")
    os.mkdir(outputdir+"\\10_INTRODUSE_RAPOARTE")
    os.mkdir(outputdir+"\\11_Negasite")
except FileExistsError:
    pass

try:
    os.makedirs(rapoarte)
except FileExistsError:
    pass


server = 'outlook.office365.com'
user = 'facturi.medici@reginamaria.ro'
password = 'WGH@e-wV6+'
outputdir = 'C:\\Users\\quasar\\invoice_handling\\'+folder+'\\1.0_EMAIL_DUMP'
subject = '' #subject line of the emails you want to download attachments from

# connects to email client through IMAP
def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    m.select()
    return m


# for msg in m.fetch():c
#     print(msg.date_str)
# downloads attachment for an email id, which is a unique identifier for an
# email, which is obtained through the msg object in imaplib, see below
# subjectQuery function. 'emailid' is a variable in the msg object class.

def downloaAttachmentsInEmail(m, emailid, outputdir):
    resp, data = m.fetch(emailid, "(BODY.PEEK[])")
    
    email_body = data[0][1]
    # print("email body: ", email_body)
    mail = email.message_from_bytes(email_body)
    # print(mail)

    # if mail.get_content_maintype() != 'multipart':
    #     return
    numar = 0
    # for part in mail.walk():
    #     fileName = part.get_filename()
    #     print("NUMELE FISIERULUI: ",fileName)
    numarator = 0
    for part in mail.walk():
        numarator = numarator + 1
        
        fileName = part.get_filename()
        numar = numar + 1
        print(numar)
        print("NUMELE FISIERULUI: ",fileName)
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None: #if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            # filename = part.get_filename()
            downloadeaza = False
            
            # print(part)
            try:
                fileName.strip("/")
                fileName.strip("\\")
                fileName.rstrip("\n")
                fileName.rstrip("\r")
                
                # fileName.replace("ERO", "") # !!!!!!!!!!!!!!!!!!!!!!!!!!1    
                print("NUMELE FISIERULUI: ",fileName)
                words_in_title = fileName.lower().split()
                downloadeaza = True
                # for i in range(0,len(lista_cuvinte_de_nedownloadat)):
                #     for j in range(0, len(words_in_title)):
                #         if lista_cuvinte_de_nedownloadat[i] == words_in_title[j]:
                            
                #             downloadeaza = False
                print("inainte de if downloadeaza true")
                if downloadeaza == True:
                    print("imediat dupa if doenlaodeaza")
                    print("lungimea este de:     ++++++++++    ",len(fileName))
                    # for i in range(0, len(fileName)):
                    #     print(fileName[i])
                    if fileName[0]=='=':
                        fileName = fileName.replace("=?UTF-8?b?", "")
                        fileName = fileName.replace("=?utf-8?b?", "")
                        fileName = fileName.replace("=?UTF-8?B?", "")
                        fileName = fileName.replace("=?utf-8?B?", "")
                        fileName = fileName.replace("\n", "")
                        fileName = fileName.replace("\r", "")
                        print("dupa filename egal filename")
                        try:
                            b = base64.b64decode(fileName)
                        except Exception:
                            print(Exception)
                            pass
                        print("b=")
                        try:
                            s = b.encode('utf-8').strip()
                        except AttributeError:
                            pass
                        except UnboundLocalError:
                            print("UNBOUND LOCAL ERROR 1")
                            pass
                        print("s=1")
                        try:
                            s = b.decode("utf-8") #asta e un nume defisier, pe astea nu le ia, extrem de rar: =?UTF-8?Q?Polita_asigurare=5FDr_Nicoar?=    =?UTF-8?Q?=C4=83=2Epdf?=
                        except UnicodeDecodeError:
                            pass
                        except UnboundLocalError:
                            print("UNBOUND LOCAL ERROR 2")
                            pass
                        
                        print("s=2")
                        try:
                            fileName = s
                        except UnboundLocalError:
                            pass
                        print("in primu if")
                    # if fileName.startswith("b="):
                    #     fileName = fileName.replace("b=?UTF-8?b?", "")
                    #     fileName = fileName.replace("b=?utf-8?b?", "")
                    #     fileName = fileName.replace("b=?UTF-8?B?", "")
                    #     fileName = fileName.replace("b=?utf-8?B?", "")
                    #     print("dupa filename egal filename")
                    #     b = base64.b64decode(fileName)
                    #     print("b=")
                    #     s = b.encode('utf-8').strip()
                    #     # print("s=1")
                    #     s = b.decode("utf-8")
                    #     print("s=2")
                        
                    #     fileName = s
                    # print('dupa primu if')
                    if mail['Subject']=='=':
                        mail['Subject'] = mail['Subject'].replace("=?UTF-8?b?", "")
                        mail['Subject'] = mail['Subject'].replace("=?utf-8?b?", "")
                        mail['Subject'] = mail['Subject'].replace("=?UTF-8?B?", "")
                        mail['Subject'] = mail['Subject'].replace("=?utf-8?B?", "")
                        b = base64.b64decode(fileName)
                        s = b.encode('utf-8').strip()
                        s = b.decode("utf-8")
                        
                        mail['Subject'] = s
                        print("in al doilea if")
                    print('dupa al doilea if')
                    # print(fileName)
                    try:
                        if fileName.endswith(".pdf") or fileName.endswith(".PDF"):
                            # print(fileName)
                            open(outputdir + '\\' + fileName, 'wb').write(part.get_payload(decode=True))
                            # print(mail['Date'])
                            # print(fileName)
                            # print(mail['Subject'])
                            var_data =  mail['Date']
                            print("in al treilea if")

                            if mail['Date'] == None:
                                var_data = 'NULL'
                            var_nume_fisier = fileName
                            
                            if fileName == None:
                                var_nume_fisier = 'NULL'
                            var_subiect = mail['Subject']

                            if mail['Subject'] == None:
                                var_subiect = 'NULL'
                            print(mail["Date"], var_nume_fisier, var_subiect)
                            print("la sfarsit")
                        else:
                            print("a intrat in else de la .pdf")
                    except OSError:
                        # now = datetime.datetime.now()
                        # string_i_want=('%02d:%02d.%d'%(now.minute,now.second,now.microsecond))[:-2]
                        try:
                            fileName = fileName[-5:]
                            fileName = str(numarator) + str(random.randrange(100000000)) + fileName
                            open(outputdir + '\\' + fileName, 'wb').write(part.get_payload(decode=True))
                            print(fileName)
                        except PermissionError:
                            fileName = fileName[-5:]
                            fileName = numarator + str(random.randrange(100000000)) + fileName
                            print(fileName)
                            open(outputdir + '\\' + fileName, 'wb').write(part.get_payload(decode=True))
                        # return var_data, var_nume_fisier, var_subiect         
            except AttributeError:
                # now = datetime.datetime.now()
                # string_i_want=('%02d:%02d.%d'%(now.minute,now.second,now.microsecond))[:-4]
                # fileName = "nume_problematic"+ string_i_want+'.pdf'
                try:
                    print("a intrat la al doilea download")
                    open(outputdir + '\\' + fileName, 'wb').write(part.get_payload(decode=True))
                    print("AttributeError")
                except TypeError:
                    print("TYPE ERROR, nu e string, e nonetype")
                # return "AttributeError","",""
            # except OSError:
            #     #!!!!!!!!!!!!!!!!!!!!!!! ATENTIE FACTURILE CU \n \r nu sunt downloadate ; de ex: 'FACTURA 027 DIN 02.10.2020 -\r\n SERVICII MEDICALE SEPT 2020 DR. MAIER TRAIAN.pdf'
            #     #  de rezolvat
            #     print("os error")
                # return "OSError","",""
    return #msg['Date'], mail[subject], filename
        # else:    
        #     return "NU", "ARE", "ATASAMENT"
    # return msg['Date']

# download attachments from all emails with a specified subject line
# as touched upon above, a search query is executed with a subject filter,
# a list of msg objects are returned in msgs, and then looped through to
# obtain the emailid variable, which is then passed through to the above
# downloadAttachmentsinEmail function

def subjectQuery(subject):
    m = connect(server, user, password)
    m.select("Inbox")
    # typ, msgs = m.search(None, '(SINCE '+mail_search_de_cand+' BEFORE '+mail_search_pana_cand+')','(SUBJECT "' + subject + '")') #, , '(FROM "badicrin@yahoo.co.uk")' BEFORE "14-Dec-2020"
    typ, msgs = m.search(None, '(SINCE 18-Jun-2021 BEFORE 21-Jun-2021)','(SUBJECT "'+subject+'")')
    msgs = msgs[0].split()
    with open('C:\\Users\\quasar\\invoice_handling\\2021\\email_log.txt','w') as csv:
        csv.write('DATA,SUBIECT,NUME FISIER,DOWNLOADAT\n')
        # write.writerow(['DATA','SUBIECT', 'NUME FISIER', "DOWNLOADAT"])
        for emailid in msgs:
            a=downloaAttachmentsInEmail(m, emailid, outputdir)
            scrie = ''
            
            try:
                
                scrie += a[0]
                scrie +=","
                scrie += a[1]
                scrie +=","
                a[2].replace("\r","")
                a[2].replace("\n","")
                scrie += a[2]
                scrie +=","
                print(a)
                scrie +='\n'
                csv.write(scrie)
            except TypeError:
                print("EROARE jos -------------------------------------------------")
                print(a)
                # csv.write("EROARE \n")
                try:
                    csv.write(a[0])
                except TypeError:
                    pass
                try:
                    csv.write(a[1])
                except TypeError:
                    pass
                try:
                    csv.write(a[2])
                except TypeError:
                    pass
                

subjectQuery(subject)
csv.writer
# def downloadAllAttachmentsInInbox(server, user, password, outputdir):
#     m = connect(server, user, password)
#     resp, items = m.search(None, "(ALL)")
#     items = items[0].split()
#     for emailid in items:
#         downloaAttachmentsInEmail(m, emailid, outputdir)

# downloadAllAttachmentsInInbox(server, user, password, outputdir)