import markdown
import bleach
from markdownify import markdownify


def bleach_md(markdown_content):
    allowed_tags = ["p", "a", "code", "pre", "blockquote", "strong", "em", "br", "b", "i", "ul", "li"]
    allowed_attributes = {"code": ["class"], "a": "href"}
    if not markdown_content:
        return markdown_content
    cleaned = bleach.clean(markdown.markdown(markdown_content, extensions=['fenced_code', 'codehilite']),
                           tags=allowed_tags, attributes=allowed_attributes)
    return cleaned


def html_to_md(content):
    return markdownify(content)
