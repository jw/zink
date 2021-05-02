from django import template
import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name

register = template.Library()


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return f'<pre><code>{mistune.escape(code)}</code></pre>'


@register.filter
def markdown(value):
    markdown = mistune.Markdown(renderer=HighlightRenderer())
    return markdown(value)
