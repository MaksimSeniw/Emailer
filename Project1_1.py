import time
import email
import imaplib
from email.header import decode_header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
EMAIL = 'seniwprogramming@gmail.com'
PASSWORD = 'oxvpftwlkwvejaud'
SERVER = 'imap.gmail.com'
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')
status, data = mail.search(None, 'ALL')
mail_ids = []
for block in data:
    mail_ids += block.split()
for i in mail_ids:
    status, data = mail.fetch(i, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])
            mail_from = message['from']
            mail_subject = message['subject']
            if message.is_multipart():
                mail_content = ''
                for part in message.get_payload():
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                mail_content = message.get_payload()
            #print(f'From: {mail_from}')
            #print(f'Subject: {mail_subject}')
            #print(f'Content: {mail_content}')

ounces_drank = [int(s) for s in mail_content.split() if s.isdigit()]
ounces_drank.remove(2022)
ounces_drank = [str(integer) for integer in ounces_drank]
ounces_drank = "".join(ounces_drank)
ounces_drank = int(ounces_drank)
#print(ounces_drank)
def email_response():
    ctx = ssl.create_default_context()
    password = "oxvpftwlkwvejaud"    
    sender = "seniwprogramming@gmail.com"    
    receiver = mail_from
    message = MIMEMultipart("mixed")
    message["Subject"] = "Hydration"
    message["From"] = sender
    message["To"] = receiver
    message.attach(MIMEText("You have drank " + str(ounces_drank) + " ounces. You should drink " + str(125 - ounces_drank) + " more to hit recommended targets.", "plain"))
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
def delete_email():
    username = "seniwprogramming@gmail.com"
    password = "oxvpftwlkwvejaud"
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    imap.select("INBOX")
    status, messages = imap.search(None, 'SUBJECT "Hydration"')
    messages = messages[0].split(b' ')
    for mail in messages:
        _, msg = imap.fetch(mail, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                print("Deleting", subject)
        imap.store(mail, "+FLAGS", "\\Deleted")
    imap.expunge()
    imap.close()
    imap.logout()
while(True):
    email_response()
    delete_email()
    time.sleep(240)