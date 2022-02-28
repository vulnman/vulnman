import markdown


def md_to_tex(value):
    return markdown.markdown(value, extensions=[LaTeXExtension()])
