import logging

import mistune
from django import template
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

logger = logging.getLogger(__name__)

register = template.Library()


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if not lang:
            first_line, _, code = code.partition("\n")
            name = first_line.replace(":", "")
            try:
                lexer = get_lexer_by_name(name, stripall=True)
                formatter = html.HtmlFormatter()
                return highlight(code, lexer, formatter)
            except ClassNotFound as e:
                return f"<pre><em>{e}</em><code>{mistune.escape(code)}</code></pre>"
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


@register.filter
def markdown(value):
    markdown = mistune.Markdown(renderer=HighlightRenderer())
    return markdown(value)
