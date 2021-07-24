import textwrap
from typing import Optional

from bloglang import ast

from . import hook


@hook.impl(trylast=True)
def handle_spec(spec: str) -> Optional[ast.Spec]:
    return ast.Spec(spec)


@hook.impl(trylast=True)
def handle_specdent(spec: str, inner_text: str) -> Optional[ast.Specdent]:
    return ast.Specdent(spec, textwrap.dedent(inner_text))
