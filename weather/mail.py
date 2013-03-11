#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: mail.py
#@author : wklken@yeah.ent
#@version : 0.1
#@desc: module for sending mail.

import sys
import smtplib

#from email.MIMEMultipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
#from email.mime.MIMEBase import MIMEBase
from email.mime.base import MIMEBase
#from email.MIMEText import MIMEText
from email.mime.text import MIMEText
#import email.Encoders as encoders
from email import encoders

def send_mail(mail_from, mail_to, subject, msg_txt, files=[]):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = mail_to
 
    # Create the body of the message (a plain-text and an HTML version).
    #text = msg
    html = msg_txt
 
    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html', 'utf-8')
 
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)
 
    #attachment
    for f in files:
        #octet-stream:binary data
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(f, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    
    mailto_list = mail_to.strip().split(",")
    if len(mailto_list) > 1:
        for mailtoi in mailto_list:
            s.sendmail(mail_from, mailtoi.strip(), msg )
    else:
        s.sendmail(mail_from, mail_to, msg.as_string())

    s.quit()
    return True

if __name__ == '__main__':
	mail_from = 'shenhd@duliodev.com'
	mail_to = 'huadu.shen@yahoo.com'
	title = 'Test Email'
	text = '<h1>test email</h1>'
	send_mail( mail_from, mail_to, title, text )
