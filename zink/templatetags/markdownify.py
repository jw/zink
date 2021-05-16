import logging

from django import template
import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

logger = logging.getLogger(__name__)

register = template.Library()


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        logger.warning(f"code: [{code}]")
        first_line, _, code = code.partition('\n')
        name = first_line.replace(":", "")
        try:
            lexer = get_lexer_by_name(name)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        except ClassNotFound as e:
            return f'<pre><em>{e}</em><code>{mistune.escape(code)}</code></pre>'


@register.filter
def markdown(value):
    markdown = mistune.Markdown(renderer=HighlightRenderer())
    return markdown(value)
