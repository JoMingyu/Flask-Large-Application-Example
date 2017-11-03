# -*- coding: utf-8 -*-

from smtplib import SMTP
from email.mime.text import MIMEText


class Mail:
    def __init__(self, smtp_url, smtp_port):
        """
        :type smtp_url: str
        :type smtp_port: int
        """
        self.smtp = SMTP(smtp_url, smtp_port)
        # Refer Config
        self.smtp_id = ''

        self.smtp.starttls()

        # Refer Config : smtp email, smtp pw
        # self.smtp.login('', '')

    def send(self, subject, content, receiver_email):
        msg = MIMEText(content, _charset='utf-8')

        msg['subject'] = subject
        # Refer Config
        msg['from'] = self.smtp_id
        msg['to'] = receiver_email

        self.smtp.sendmail('', receiver_email, msg.as_string())

    def __del__(self):
        self.smtp.quit()
