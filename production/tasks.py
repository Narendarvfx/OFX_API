import smtplib

from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from celery.exceptions import Retry
from django.template.loader import get_template

from OFX_API import settings
from OFX_API.settings import DEFAULT_FROM_EMAIL
import logging
from datetime import datetime

@shared_task(bind=True, autoretry_for=(smtplib.SMTPException, ConnectionError, TimeoutError), retry_backoff=10,
             max_retries=3)
def send_notification_mail(self, context={}, template=None, subject=str, to_addr=[], cc_addr=[], reply_to=[]):
    try:
        message = get_template(template).render(context)
        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email=DEFAULT_FROM_EMAIL,
            to=to_addr,
            cc=cc_addr,
            reply_to=reply_to,
        )
        mail.content_subtype = "html"

        logging.info(f"Attempting to send email to {to_addr}")

        result = mail.send()

        if result == 0:
            error_msg = "Failed to send email"
            logging.error(error_msg)
            raise smtplib.SMTPException(error_msg)  # Ensure failure is raised

        logging.info(f"Email sent successfully to {to_addr}")
        return {"status": "success", "message": "Email sent successfully"}

    except smtplib.SMTPException as e:
        print(e)
        logging.error(f"SMTPException: {str(e)} - Retrying...")

        # Raise self.retry() properly so Celery marks it as "RETRY"
        raise self.retry(exc=e, countdown=10)

    except Exception as e:
        print(e)
        logging.error(f"Unexpected error: {str(e)}")

        # Raise exception so Celery marks it as "FAILED"
        raise e