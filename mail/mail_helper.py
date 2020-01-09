from mailjet_rest import Client
import os
import logging
import threading
import time
from humanfriendly import format_timespan
# Get your environment Mailjet keys
API_KEY = os.environ.get('MJ_APIKEY_PUBLIC', default='example')
API_SECRET = os.environ.get('MJ_APIKEY_PRIVATE', default='example')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', default='example@example.com')
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')



def send_arch_message(user, mail, file_name='NOT_GIVEN', password=None, time=0, additional_info=None):
    message = None
    subject = "Archive cracker"
    time = format_timespan(time)
    if password is None:
        message = f"""
        <h3>
            Your decoding task has not been completed
        </h3><br>
        <div>
            Sorry but your archive named <b>\'{file_name}\'</b> couldn't be cracked in <i><b>{time}<b></i> 
        </div>
        """
    else:
        pass_message = ''
        if password == 'EMPTY_PASSWORD':
            pass_message = "Your archive has no password"
        else:
            pass_message = f"The password for your archive is: <i><b>{password}</b></i><br>"
        message = f"""
        <h3>
            Your decoding task has been completed
        </h3><br>
        <div>
            {pass_message}
        </div>
        <div>
            Your archive named <i><b>\'{file_name}\'<b></i> was cracked in <i><b>{time}<b></i>
        </div>
        """
    if not additional_info is None:
        message = message + f"""<div>{additional_info}</div>"""
    data = {
        'Messages': [
                    {
                    "From": {
                        "Email": f"{SENDER_EMAIL}",
                        "Name": "Developer"
                    },
                    "To": [
                        {
                        "Email": f"{mail}",
                        "Name": f"{user}"
                        }
                    ],
                    "Subject": f"{subject}",
                    "TextPart": None,
                    "HTMLPart": message,
                    "CustomID": "ArchiveID"
                    }
                ]
    }
    send_mail(data)


def send_mail(data):
    logging.info("[MAIL] Sending email")
    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        logging.info("[MAIL] Successfully sent mail")
    else:
        logging.error("[MAIL] Something went wrong: " + result.raw)
