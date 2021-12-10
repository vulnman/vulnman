import markdown
import bleach
from markdownify import markdownify


def bleach_md(markdown_content):
    allowed_tags = ["p", "a", "code", "pre", "blockquote", "h1", "h2", "h3", "h4", "h5", "strong", "em"]
    allowed_attributes = {"code": ["class"], "a": "href"}
    if not markdown_content:
        return markdown_content
    cleaned = bleach.clean(markdown.markdown(markdown_content),
                           tags=allowed_tags, attributes=allowed_attributes)
    return cleaned


def html_to_md(content):
    return markdownify(content)
