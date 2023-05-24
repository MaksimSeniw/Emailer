import imaplib
import email
from email.header import decode_header

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