import os
import smtplib

from flask import url_for


def send_email(email, code):
    server = smtplib.SMTP(os.environ['EMAIL_SERVER'], 587)
    server.starttls()

    server.login(os.environ['EMAIL_LOGIN'], os.environ['EMAIL_PASSWORD'])

    msg = """From: {} <{}>
To: <{}>
Subject: Password Reset for {}


Hello!
    
Here is the reset code for your account on GFPAuth.
    
Please go to {}{}?authcode={}
    
Thanks.""".format(os.environ['EMAIL_FROM_NAME'], os.environ['EMAIL_FROM_MAIL'],
                  os.environ['SITE_NAME'],
                  email,
                  os.environ['SITE_URL'],
                  url_for('password.reset'),
                  code)

    server.sendmail(os.environ['EMAIL_FROM_MAIL'], email, msg)
