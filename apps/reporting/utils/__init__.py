

class ReportError(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url


def get_report_errors(release):
    errors = []
    print(release.project)
    print(release.project.get_assets())
    for asset in release.project.get_assets():
        print(asset)
        print(asset.description)
        if not asset.description:
            errors.append(ReportError("Asset %s does not have a description set", "#scope"))
    return errors
