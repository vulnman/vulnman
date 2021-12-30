import os


class ReportSection(object):

    def __init__(self, title, template_file, content_file=None):
        self.title = title
        self.template_file = template_file
        self.content_file = content_file

    def get_content_file_path(self, report_template_directory):
        return os.path.join(report_template_directory, "contents/%s" % self.content_file)

    def get_content(self, report_template_directory):
        path = self.get_content_file_path(report_template_directory)
        with open(path, "r") as content_f:
            return content_f.read()

    def get_template_file_path(self, report_template_directory):
        path = os.path.join(report_template_directory, "sections/%s" % self.template_file)
        return path


class ReportTemplate(object):
    name = None
    template_directory = None
    sections = None
    stylesheets = []

    def get_name(self):
        if not self.name:
            raise Exception("No name set")
        return self.name

    def get_sections(self):
        if not self.sections:
            raise Exception("No sections set")
        return self.sections.copy()

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

    def get_sections_directory(self):
        return os.path.join(self.get_template_directory(), "sections/")
