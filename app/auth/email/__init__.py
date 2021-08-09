import os
import smtplib

from flask import url_for


def validate_environment():
    return ('EMAIL_SERVER' in os.environ) & ('EMAIL_LOGIN' in os.environ) & ('EMAIL_PASSWORD' in os.environ) & (
            'EMAIL_FROM_NAME' in os.environ)


def send_email(email, code):
    server = smtplib.SMTP(os.environ['EMAIL_SERVER'], os.environ['EMAIL_PORT'])
    if os.environ['EMAIL_TLS'] != "False":  # We have to be REALLY explicit
        server.starttls()

    server.login(os.environ['EMAIL_LOGIN'], os.environ['EMAIL_PASSWORD'])

    msg = f"""From: {os.environ['EMAIL_NAME']} <{os.environ['EMAIL_FROM']}>
To: <{email}>
Subject: Password Reset for {os.environ['SITE_NAME']}


Hello!
    
Here is the reset code for your account on {os.environ['SITE_NAME']}.
    
Please go to {os.environ['SITE_URL']}{url_for('password.reset')}?authcode={code}
    
Thanks."""

    print(f"Sending a password reset for email: {email}")
    server.sendmail(os.environ['EMAIL_FROM'], email, msg)
    server.close()
