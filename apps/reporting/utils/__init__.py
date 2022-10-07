

class ReportError(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url


def get_report_errors(release):
    errors = []
    for asset in release.project.get_assets():
        if not asset.description:
            errors.append(ReportError("Asset %s does not have a description set", "#scope"))
    return errors
