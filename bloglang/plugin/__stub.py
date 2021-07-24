from typing import Optional

from bloglang import ast

from . import hook


@hook.spec(firstresult=True)
def handle_spec(spec: str) -> Optional[ast.Spec]:
    """Hook me"""


@hook.spec(firstresult=True)
def handle_specdent(spec: str, inner_text: str) -> Optional[ast.Specdent]:
    """Hook me"""
