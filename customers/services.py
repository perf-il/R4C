from django.core.mail import send_mail

from R4C import settings


def send_mail_to_customers(subject, body, customers_list):
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=customers_list
    )
