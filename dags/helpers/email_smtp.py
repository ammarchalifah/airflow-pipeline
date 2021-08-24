import smtplib
import os
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(recipient, subject, body):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    s = smtplib.SMTP(host='mail.ammarchalifah.com', port=26)
    s.starttls(context=context)
    s.login(os.environ['SMTP_EMAIL_ADDRESS'], os.environ['SMTP_EMAIL_PASSWORD'])

    msg = MIMEMultipart()

    message = body

    msg['From']=os.environ['SMTP_EMAIL_ADDRESS']
    msg['To']=recipient
    msg['Subject']=subject

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    
    del msg