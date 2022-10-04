from django.utils.module_loading import import_string
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from apps.responsible_disc import models
from apps.reporting.tasks import export_single_vulnerability


def export_advisory(vulnerability):
    # returns a text or zip file
    # and a boolean that is set to true if it is a zip file
    template_name = vulnerability.advisory_template
    Report = import_string(settings.REPORT_TEMPLATES.get(template_name, "default") + ".advisory.Report")
    obj = Report(None, template_name=template_name, vulnerability=vulnerability)
    raw_source, is_zip = obj.generate_report()
    return raw_source, is_zip


def notify_vendor(vulnerability_pk):
    vulnerability = models.Vulnerability.objects.get(pk=vulnerability_pk)
    # TODO: do not hardcode this one
    pdf_source = export_single_vulnerability(vulnerability, vulnerability.advisory_template)
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
