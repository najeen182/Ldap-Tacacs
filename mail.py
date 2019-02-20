import os                                                                                                                                                                                             
import smtplib
import sys

from email.mime.text import MIMEText
from template import template
def error(msg):
    sys.stderr.write(msg + "\n")

def send_custom_mail(email,username,password):

    msg1 = '''
        <b>Dear {0}</b>,<br>
        Your Log User Has been created. Following are your credential, Please manage to change the password:<br>
        username : {1}<br>
        password : {2} <br>
        '''.format(email,username,password)

    msg = MIMEText(msg1,'html')

    sender = "Server<server@worldlink.com.np>"
    rcpt = "{0}@worldlink.com.np".format(email)
    subject = "Regarding Log Credential"
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = rcpt

    server = smtplib.SMTP("smtp.wlink.com.np")
    server.sendmail(sender, [rcpt], msg.as_string())
    server.quit()


