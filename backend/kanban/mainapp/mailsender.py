from django.core.mail import send_mail
from kanban.settings import EMAIL_HOST_USER

def send_for_verify(to_send, url):
    message = f"Please verify your account!\n\n{url}"
    recipient_list = [ to_send, ]

    try:
        send_mail(
                'Subject',
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )
    except Exception as ex:
        return print(ex)

def send_to_reset_password(to_send, url):
    message = f"Please reset your password for your account!\n\n{url}"
    recipient_list = [ to_send, ]

    try:
        send_mail(
                'Subject',
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )
    except Exception as ex:
        return print(ex)

def send_to_complite_signup(to_send, url):
    message = f"Your accont has been created!\nPlease complite your sign up!\n\n{url}"
    recipient_list = [ to_send, ]

    try:
        send_mail(
                'Subject',
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )
    except Exception as ex:
        return print(ex)
