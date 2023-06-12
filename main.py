import time
from iss import Iss
import asyncio
import re
from email.message import EmailMessage
from typing import Tuple, Union
import aiosmtplib

EMAIL = "xxx@xxxx.com"
PASSWORD = "xxx"
HOST = "smtp.gmail.com"

CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
}

iss = Iss()


def send_email():
    print("Sending email.")

    message = EmailMessage()
    message["From"] = "ISS Notifier"
    message["To"] = EMAIL
    message["Subject"] = "Look Up!"
    message.set_content("The ISS is above you.")

    send_kws = dict(username=EMAIL, password=PASSWORD, hostname=HOST, port=587, start_tls=True)
    asyncio.run(aiosmtplib.send(message, **send_kws))


# pylint: disable=too-many-arguments
async def send_txt(
        num: Union[str, int],
        carrier: str,
        email: str,
        pword: str,
        msg: str,
        subj: str
) -> Tuple[dict, str]:
    to_email = CARRIER_MAP[carrier]

    # build message
    message = EmailMessage()
    message["From"] = email
    message["To"] = f"{num}@{to_email}"
    message["Subject"] = subj
    message.set_content(msg)

    # send
    send_kws = dict(username=email, password=pword, hostname=HOST, port=587, start_tls=True)
    res = await aiosmtplib.send(message, **send_kws)  # type: ignore
    msg = "failed" if not re.search(r"\sOK\s", res[1]) else "succeeded"
    print(msg)
    return res


def send_txt_msg():
    _num = "1234567890"
    _carrier = "verizon"
    _email = EMAIL
    _pword = PASSWORD
    _msg = "Look up!"
    _subj = "The ISS is above you."
    coro = send_txt(_num, _carrier, _email, _pword, _msg, _subj)
    asyncio.run(coro)


while True:
    iss.update_info()
    iss.display_info()
    if iss.is_visible():
        send_email()
        send_txt_msg()
        time.sleep(420)
    else:
        print("Not found, waiting for 1 minute...")
        time.sleep(60)
