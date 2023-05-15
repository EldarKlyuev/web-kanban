import smtplib
import os

def send_email(to_send, url):
    sender = os.getenv("EMAIL_HOST_USER")
    password = os.getenv("EMAIL_HOST_PASSWORD")

    message = f"{url}"

    server = smtplib.SMTP("smtp.mail.ru", 2525)

    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, to_send, message)

        return print("The message sent")
    except Exception as _ex:
        return print(f"{_ex}\nCheck login")