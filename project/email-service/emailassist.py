import smtplib
import re
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'mail.sender.osp@mail.ru'
PASSWORD = os.getenv('MAIL_PASSWORD')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class EmailSender():
    def __init__(self, address, password):
        self.smtp_client = smtplib.SMTP(host='smtp.mail.ru', port=587)
        self.smtp_client.starttls()
        self.smtp_client.login(address, password)
        self.address = address

    def send_email(self, send_to, body):
        self.check(send_to)

        msg = MIMEMultipart()

        msg['From'] = self.address
        msg['To'] = send_to
        msg['Subject'] = "RABBITMQPrikol"

        msg.attach(MIMEText(body, 'plain'))

        self.smtp_client.send_message(msg)
        del msg

    def check(self, email):
        if re.fullmatch(regex, email) is None:
            raise ValueError("Invalid Email")

    def close(self):
        self.smtp_client.quit()

