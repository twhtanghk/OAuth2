from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
import requests
import logging

logger = logging.getLogger(__name__)

class Notes(BaseEmailBackend):
    def send_messages(self, email_messages):
        for msg in email_messages:
            r = requests.post(settings.EMAIL_HOST, data=msg.__dict__, verify=False)
            if r.status_code != 201:
                logger.error('{0}: {1}'.format(str(msg.to), msg.subject))
                raise Exception("mail not successfully sent")