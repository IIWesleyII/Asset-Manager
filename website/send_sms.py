from twilio.rest import Client
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
# the following line needs your Twilio Account SID and Auth Token
client = Client(os.getenv('SMS_ACCOUNT_SID'), os.getenv('SMS_AUTH_TOKEN'))

def send_sms_code(phone_num, sms_verification_code):
    '''
    - send verification code to user phone number
    '''
    client.messages.create(to=phone_num, 
                        from_=os.getenv('SMS_FROM'), 
                        body=f"{sms_verification_code}")
                       
    print(f'sms code: {sms_verification_code}')


def send_email_code(email,email_verification_code):
    '''
    - send verification code to user email
    '''
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = 'Asset Manager password recovery'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    msg.set_content(f'Your email recovery code is: {email_verification_code}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print(f'email code: {email_verification_code}')