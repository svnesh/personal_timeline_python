import configparser
import datetime as dt
import time
import os
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

import base64
from googleapiclient.discovery import build
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

myData = []
myEvent = {}
today = dt.date.today()     

config = configparser.RawConfigParser()
config.read('credentials.ini')
email = config.get('credentials', 'username')

SCOPES = 'https://www.googleapis.com/auth/gmail.send'

#####  Functions start  ###########

def getCredentials():
    creds=None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(\
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print('Storing credentials')
    return creds

def createMessage(sender, to, subject, message_htmltext, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    #message.attach(MIMEText(message_text, 'plain'))
    message.attach(MIMEText(message_htmltext, 'html'))
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw':raw}

def sendmail(sender, to, subject, message_htmltext, message_text):
    print('[started to send mail]')
    credentials = getCredentials()
    service = build('gmail', 'v1', credentials=credentials)
    sendingMessage = createMessage(sender, to, subject, message_htmltext, message_text)
    try:
        message = (service.users().messages().send(userId=sender, body=sendingMessage)\
            .execute())
        print('Message id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

#####  Functions end ######

def main():
    print('[Start reading events]')
    with open ('datesData.txt', 'r') as f:
        data = f.readlines()
    data = [json.loads(x.strip()) for x in data]
    print('[converted events to json]')

    for event in data:
        strDate = str(event['Date']).split('-') #YYYY-mm-dd
        myDate = dt.date(int(strDate[0]), int(strDate[1]), int(strDate[2]))
        reminder = int(event['Reminder'])
        message = event['Message']
        message_html = event['Messagehtml']
        subject = event['Name']

        daysRemain = myDate - today
        if ((myDate > today) and (daysRemain.days <= reminder) and (daysRemain.days > 0)):
            message = f'{message}{daysRemain.days} days'
            message_html = f'{message_html}{daysRemain.days} days'
            sendmail(email, email, subject, message_html, message)

if __name__ == "__main__":
    main()