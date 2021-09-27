import smtplib
import pandas as pd
#from email.mime.multipart import MIMEMultipart
import datetime
from email.mime.multipart import MIMEMultipart
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# from email.MIMEBase import MIMEBase
# #from mailer_code import mailer
# from email import Encoders

def mailer(body,recipients,Subject="Password reset link"):

    message = Mail(
    from_email='contactus@spectevo.com',
    to_emails=recipients,
    subject=Subject,
    html_content=body)
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)




# mailer("hello","gaurav.singh@sigmoidstar.com")