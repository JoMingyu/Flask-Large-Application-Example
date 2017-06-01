# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

from_email = ''
smtp_host = ''
smtp_port = 0
smtp_id = ''
smtp_pw = ''


def send(to_email, title, content):
    message = MIMEText(content, _charset='utf-8')
    message['Subject'] = title
    message['From'] = from_email
    message['To'] = to_email

    s = smtplib.SMTP(smtp_host, smtp_port)
    s.starttls()
    s.login(smtp_id, smtp_pw)
    s.sendmail(from_email, to_email, message.as_string())
    s.close()
