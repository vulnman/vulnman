from django_tex.environment import environment
import markdown
from apps.reporting.utils.mdtex import LaTeXExtension


def md_to_tex(value):
    return markdown.markdown(value, extensions=[LaTeXExtension()])


def tex_report_env(**options):
    env = environment(**options)
    env.filters.update({
        'md_to_tex': md_to_tex
    })
    return env
