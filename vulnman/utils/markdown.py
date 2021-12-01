import markdown
import bleach


def bleach_md(markdown_content):
    allowed_tags = ["p", "a", "code", "pre", "blockquote", "h1", "h2", "h3", "h4", "h5", "strong", "i"]
    allowed_attributes = {"code": ["class"], "a": "href"}
    cleaned = bleach.clean(markdown.markdown(markdown_content), tags=allowed_tags, attributes=allowed_attributes)
    return cleaned
