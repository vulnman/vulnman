import markdown
import bleach
import re
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from markdown.extensions.codehilite import CodeHiliteExtension
from markdownify import markdownify
from django.utils.safestring import mark_safe


class HighlightCodeBlockProcessor(Postprocessor):
    line = re.compile(r'(<span id="line-\d+">(?:<span class="hll">)?(?:<span class="linenos">\s*\d+<\/span>)?)([^><]+)((?:<\/span>)+)',
        re.DOTALL | re.MULTILINE)
    highlited_code = re.compile(r"§§(.*?)§§")

    @staticmethod
    def match_bold(code):
        bold = HighlightCodeBlockProcessor.highlited_code.sub(r"<b>\1</b>", code.group(2))
        return "%s%s%s" % (code.group(1), bold, code.group(3))

    def run(self, text):
        return self.line.sub(self.match_bold, text)


class HighlightCodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(HighlightCodeBlockProcessor(md), "highlightcodeblockprocessor", 30)


def bleach_md(markdown_content):
    allowed_tags = ["p", "a", "code", "pre", "blockquote", "strong", "em", "br", "b", "i", "ul", "li", "div", "span", "h4", "h5"]
    allowed_attributes = {"code": ["class"], "a": "href", "div": ["class"], "span": ["class"]}
    if not markdown_content:
        return markdown_content
    cleaned = bleach.clean(markdown.markdown(markdown_content, extensions=['fenced_code', CodeHiliteExtension(
                guess_lang=False,
                linenums=False,
                linenos="inline",
                linespans="line",
                startinline=True,
            ),HighlightCodeBlockExtension(), ]),
                           tags=allowed_tags, attributes=allowed_attributes)
    return cleaned


def html_to_md(content):
    return markdownify(content)


def md_to_clean_html(content):
    return mark_safe(bleach_md(content))
