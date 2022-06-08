from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from apps.reporting.tasks import get_stylesheets
from apps.responsible_disc import models


@shared_task
def export_single_vulnerability(vulnerability):
    context = {
        "vulnerability": vulnerability,
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
    }
    # TODO: do not hardcode this one
    report_template = "default"
    template = "responsible_disc/reporting/exported_vulnerability.html"
    raw_source = render_to_string(template, context)
    font_config = FontConfiguration()
    pdf_source = HTML(string=raw_source).write_pdf(
        stylesheets=get_stylesheets(report_template),
        font_config=font_config)
    return pdf_source


@shared_task
def export_advisory(vulnerability):
    context = {
        "vulnerability": vulnerability,
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
    }
    template = "responsible_disc/reporting/advisory.md"
    raw_source = render_to_string(template, context)
    return raw_source


@shared_task
def notify_vendor(vulnerability_pk):
    vulnerability = models.Vulnerability.objects.get(pk=vulnerability_pk)
    pdf_source = export_single_vulnerability(vulnerability)
    if not vulnerability.vendor_email:
        models.VulnerabilityLog.objects.create(
            message="No vendor email address set! Mail was not sent", vulnerability=vulnerability,
            action=models.VulnerabilityLog.ACTION_INTERNAL_LOG)
        return
    template = "responsible_disc/emails/vendor_notification.html"
    context = {"vulnerability": vulnerability}
    message = render_to_string(template, context)
    mail = EmailMessage("Vulnerability in %s" % vulnerability.affected_product, message,
                        settings.RESPONSIBLE_DISCLOSURE_MAIL_FROM, [vulnerability.vendor_email],
                        bcc=[vulnerability.user.email])
    mail.attach("details.pdf", pdf_source, "application/pdf")
    mail.send()
    models.VulnerabilityLog.objects.create(message="Notification Mail sent.",
                                           vulnerability=vulnerability,
                                           action=models.VulnerabilityLog.ACTION_VENDOR_NOTIFIED)
