import zipfile
import os
from io import BytesIO
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from apps.responsible_disc import models
from apps.reporting.tasks import export_single_vulnerability


def export_advisory(vulnerability):
    # returns a text or zip file
    # and a boolean that is set to true if it is a zip file
    context = {
        "vulnerability": vulnerability,
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
    }
    template = "advisory_templates/%s.md" % vulnerability.advisory_template
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


def notify_vendor(vulnerability_pk):
    vulnerability = models.Vulnerability.objects.get(pk=vulnerability_pk)
    # TODO: do not hardcode this one
    pdf_source = export_single_vulnerability(vulnerability, "default")
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
