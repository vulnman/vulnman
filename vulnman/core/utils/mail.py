from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader


def send_mail(subject, email_template_name, context, from_email, to_email, html_email_template_name=None):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    subject = "%s%s" % (settings.MAIL_SUBJECT_PREFIX, subject)
    body = loader.render_to_string(email_template_name, context)
    if not isinstance(to_email, list):
        to_email = [to_email]
    email_message = EmailMultiAlternatives(subject, body, from_email, to_email)
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")
    email_message.send()
