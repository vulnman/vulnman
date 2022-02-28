import markdown
import bleach
from markdownify import markdownify
from django.utils.safestring import mark_safe


def bleach_md(markdown_content):
<<<<<<< HEAD
    allowed_tags = ["p", "a", "code", "pre", "blockquote", "strong", "em", "br", "b", "i", "ul", "li", "div", "span"]
=======
    allowed_tags = ["p", "a", "code", "pre", "blockquote", "strong", "em", "br", "b", "i", "ul", "li", "div", "span", "h4", "h5"]
>>>>>>> origin/dev
    allowed_attributes = {"code": ["class"], "a": "href", "div": ["class"], "span": ["class"]}
    if not markdown_content:
        return markdown_content
    cleaned = bleach.clean(markdown.markdown(markdown_content, extensions=['fenced_code', 'codehilite']),
                           tags=allowed_tags, attributes=allowed_attributes)
    return cleaned


def html_to_md(content):
    return markdownify(content)


def md_to_clean_html(content):
    return mark_safe(bleach_md(content))
