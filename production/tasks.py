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

filename = datetime.now().strftime("%d-%m-%Y %H-%M-%S")#Setting the filename from current date and time
logging.basicConfig(filename="./email_send.log", filemode='a',
                    format="%(asctime)s, %(msecs)d %(name)s %(levelname)s [ %(filename)s-%(module)s-%(lineno)d ]  : %(message)s",
                    datefmt="%H:%M:%S",
                    level=logging.DEBUG)


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

        logging.info("Sending email")
        result = mail.send()

        if result == 0:
            raise smtplib.SMTPException("Failed to send email")

        return {"status": "success", "message": "Email sent successfully"}

    except smtplib.SMTPException as e:
        logging.error(f"Email sending failed: {str(e)}")
        raise self.retry(exc=e, countdown=10, max_retries=3)  # Retries up to 3 times

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return {"status": "failed", "message": str(e)}