import zipfile
import os
from io import BytesIO
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from apps.reporting.utils import report_gen
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
    report_generator = report_gen.ReportGenerator(report_template)
    compiled_source = report_generator.generate(raw_source)
    return compiled_source


@shared_task
def export_advisory(vulnerability, template_name):
    # returns a text or zip file
    # and a boolean that is set to true if it is a zip file
    context = {
        "vulnerability": vulnerability,
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
    }
    template = "advisory_templates/%s.md" % template_name
    if vulnerability.imageproof_set.all():
        s = BytesIO()
        with zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
            raw_source = render_to_string(template, context)
            zip_file.writestr("advisory.md", raw_source)
            # export results as zip with proof images
            for image_proof in vulnerability.imageproof_set.all():
                zip_file.write(image_proof.image.path, os.path.basename(image_proof.image.name))
        results = s.getvalue()
        return results, True
    else:
        raw_source = render_to_string(template, context)
        return raw_source, False


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
