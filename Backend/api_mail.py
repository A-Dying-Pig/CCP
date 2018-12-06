from django.core.mail import send_mail
import json
from threading import Thread

class MailThread(Thread):
    def __init__(self, title, content, address):
        super().__init__()
        self.title = title
        self.content = content
        self.address = address

    def run(self):
        with open('config.json') as f:
            mail = json.load(f)['mail']
        send_mail(self.title, 
            self.content, 
            mail['EMAIL_HOST_USER'], 
            [self.address],
        )


def sendmail(title, content, address):
    th_mail = MailThread(title, content, address)
    th_mail.start()
