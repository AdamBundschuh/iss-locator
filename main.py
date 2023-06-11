import time
from iss import Iss
import smtplib

my_email = "bundschuh.adam@gmail.com"
password = "qbgqoigohtthzftt"

iss = Iss()


def send_email():
    print("Sending email.")
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject: ISS Is Overhead!\n\nLook up."
        )


while True:
    iss.update_info()
    iss.display_info()
    if iss.is_visible():
        send_email()
        time.sleep(420)
        print("IN RANGE!")
    else:
        print("Not found, waiting for 1 minute...")
        time.sleep(60)
