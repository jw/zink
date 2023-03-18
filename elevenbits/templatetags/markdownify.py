import mistune
from django import template
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name

register = template.Library()


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code: str, lang: str) -> str:
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return f"<pre><code>{mistune.escape(code)}</code></pre>"


@register.filter
def markdown(value: str) -> str:
    markdown = mistune.Markdown(renderer=HighlightRenderer())
    return markdown(value)
