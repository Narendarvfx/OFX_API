from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template import Context

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

@shared_task(bind=True)
def send_notification_mail(self, context={},template=None, subject=str,to_addr=[], cc_addr=[], reply_to=[]):
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
    # print(mail)
    try:
        logging.info("Sending email")
        return mail.send()
    except Exception as e:
        logging.error(e)