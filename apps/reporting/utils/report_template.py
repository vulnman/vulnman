import os


class ReportTemplate(object):
    name = None
    template_directory = None
    sections = None
    stylesheets = []

    def get_name(self):
        if not self.name:
            raise Exception("No name set")
        return self.name

    def get_template_directory(self):
        if not self.template_directory:
            raise Exception("No template_directory set")
        return self.template_directory

    def get_template_path(self):
        path = os.path.join(self.get_template_directory(), "report.html")
        if not os.path.exists(path):
            raise Exception("Template file not found")
        return path

    def get_stylesheet_paths(self):
        paths = []
        for stylesheet in self.stylesheets:
            paths.append(os.path.join(self.get_template_directory(), stylesheet))
        return paths
