""" B u s i n e s s   L o g i c """

import smtplib
#import base64
smtpAddress = "smtp.office365.com"
EMAIL_ACCOUNT=""
EMAIL_PASSWORD = ""

#def decode_password():
#    return base64.b64decode(EMAIL_PASSWORD).decode()
#def encode_password(password):
#    return base64.b64encode(password)
    
#//////////////////////////////////////////////////////////////////////////////
#//SMTP////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////

def sendEmail(subject,message,user,recipient,cc):

    header = fillHeader(subject,user,recipient,cc)

    if (message == ""):
        message = 'This is a default message\n' + \
        'This is a test Email sent using Python! \n\n'
        
    msgbody = header + message

    try: 
        status,smtpserver = loginAuth(user,EMAIL_PASSWORD)
        smtpserver.sendmail(user, recipient, msgbody)
        print ('Email sent!')
        return True
    except:
        print('An error was encountered.')
        return False
        
def fillHeader(subject = "", sender = "", recipient = "", cc = "", date = ""):

    header = 'From: '   + sender    + \
    '\n' +   'To: '     + recipient + \
    '\n' +   'CC: '     + cc        + \
    '\n' +   'Subject: '+ subject   + \
    '\n\n'
    if date!="":    
        header += date              + \
    '\n\n'
    
    return header
       
def loginAuth(user,password):

    smtpserver = smtplib.SMTP(smtpAddress,587)
    smtpserver.ehlo()
    smtpserver.starttls() #Start Transport Layer Security
    smtpserver.ehlo()

    try:
        smtpserver.login(user, password)
        print ('Login success!')
        return True,smtpserver
    except:        
        print ('Login failed!')
        return False,smtpserver
    
def closeConn(smtpserver,imapAddress):
    smtpserver.close()
    imapAddress.close()
    imapAddress.logout()

#//////////////////////////////////////////////////////////////////////////////
#//IMAP////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////
import imaplib
import email
import email.header as eh
import email.message as em
import datetime as d
    
EMAIL_FOLDER = "INBOX" # DEFAULT = "INBOX"

def connectIMAP():

    M = imaplib.IMAP4_SSL('imap.outlook.com') #port=993

    try:
        rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error:
        print ('Login Failed!')
        
    return M

    
def showMail(inboxPage = 0, mailsPerPage = 4, emFolder = EMAIL_FOLDER):

    M = connectIMAP()
    
    rv, data = M.select(emFolder)
    if rv == 'OK':
        return M,processMailbox(M,inboxPage,mailsPerPage),getUnread(M)
    else:
        print("ERROR: Unable to open mailbox ", rv)    
    
def processMailbox(M,page,per):
    
    rv, data = M.search(None, "ALL")
    mail = {"id":[],"subject":[],"from":[],"date":[],"message":[]}    
    
    sortedData = (list(reversed(data[0].split()))) # reversed sorts it
    for num in sortedData[per*page:per*page+per]:  # data partition by page
        rv, data = M.fetch(num, '(BODY.PEEK[HEADER])')
        
        if rv != 'OK':
            print("ERROR getting message", num)
            return

#        status, r1 = M.fetch(num, '(FLAGS RFC822.HEADER)')////////// ideas for
#        status, r2 = M.status(num,'INBOX', "(UNSEEN)")/////////// unseen inbox
             
        mail = utilSaveMailData(mail,data,num)
         
    return mail
    
def readEmail(num,emFolder = EMAIL_FOLDER):
    
    M = connectIMAP()

    rv, data = M.select(emFolder,True) # Read-Only
    rv, data = M.search(None,"ALL")

    sortedData = (list(reversed(data[0].split())))
    num = sortedData[num]
    rv, data = M.fetch( num, '(RFC822)')
    if rv != 'OK':
        print("ERROR getting message", num)
        return 

    mail = email.message_from_bytes(data[0][1])
    
    text = []
    attachments = "none"  
    content_types =  [part.get_content_type() for part in mail.walk()]
       
    for i in range(len(content_types)):
        for part in mail.walk():
            if "application" in content_types[i]:
                attachments = "available"
            elif "text/plain" in content_types[i]:
                try:
                    text.append(part.get_payload(decode=True).decode())
                except:
                    pass

    return formatMailDisplay(mail,text,attachments)

def unscramble(string):
    if '?utf-8?' in string:
        text,encoding = eh.decode_header(string)[0]
        string = text.decode(encoding)
    return string
    
def formatMailDisplay(mail,text,attachments):
    subject = unscramble(mail["Subject"])
    date = utilGetLocalTime(mail["Date"])
    sender = unscramble(mail['From'])
    target = unscramble(mail["To"])
    text = ''.join([str(x) for x in text])
    attachments = str(attachments)          # int
    
    header = 'From: '       + sender        + \
    '\n' +   'To: '         + target        + \
    '\n' +   'Subject: '    + subject       + \
    '\n' +   'Attachments: '+ attachments   + \
    '\n\n'+  'On: '         + date          + \
    '\n\n'
    
    body = header + text
    return body
    
def utilGetLocalTime(date):
    raw_date = email.utils.parsedate_tz(date)
    local_date = d.datetime.fromtimestamp(email.utils.mktime_tz(raw_date))
    return local_date.strftime("%a, %d %b %Y %H:%M:%S")
    
def utilSaveMailData(mail,data,num): # formatting & storing
    msg = email.message_from_bytes(data[0][1])
    hdr = eh.make_header(eh.decode_header(msg['Subject']))
    mail['id'].append(num.decode())
    mail['subject'].append(str(hdr))
    mail['from'].append(str(eh.make_header(eh.decode_header(msg['From']))))
    mail['date'].append(utilGetLocalTime(msg['Date']))
    mail['message'].append(msg.get_payload())
    return mail
    
def getUnread(M):
    status, response = M.search(None, 'ALL', '(UNSEEN)')
    unread = response[0].split()
    return len(unread)
    
