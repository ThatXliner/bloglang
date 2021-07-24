from . import hook
from bloglang import ast, parser
from typing import Optional
import textwrap
import attr


@attr.s(init=False, auto_attribs=True)
class Quote(ast.Specdent):
    inner_content: ast.Document

    def __init__(self, inner_content: ast.Document) -> None:
        self.inner_content = inner_content
        self.spec = "quote"


@hook.impl(trylast=True)
def handle_specdent(spec: str, inner_text: str) -> Optional[ast.Specdent]:
    if spec == "quote":
        return Quote(parser.parse(textwrap.dedent(inner_text)))
    return None
