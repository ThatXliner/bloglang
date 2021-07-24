"""
The main parser

Implemented
============

Inline markup (with proper escaping!)
-------------------------------------

 * Code
 * Italic
 * Bold
 * Bold and italic
 * Underline
 * Strikethrough
 * Specs
 * Footnotes
 * Images
 * Links

Large markup
------------

 * Headers
 * Specdent

Partially implemented
=====================

Inline markup
-------------
 * Quotes and comments
 * The default spec library (emojis, comments, colors, code blocks...)

Unimplemented
=============

In priority order

Inline markup
-------------

 * Inline specdents

Large markup
------------

 * Lists and the like

"""
import re
import textwrap
from typing import List, NamedTuple, Optional, Dict

from bloglang import ast, plugin, escapes
from bloglang.regexes import HEADER_RE, INLINE_RE, SPECDENT_START, FOOTNOTE_CONTENT, REs


class InlineMarkup(NamedTuple):
    tokens: List[ast.Node]
    footnotes: Dict[str, Optional[ast.InlineDocument]]


def _clean(
    tokens: List[ast.Node],
    check_footnotes: bool = True,
    footnotes: Optional[Dict[str, Optional[ast.InlineDocument]]] = None,
) -> List[ast.Node]:
    output: List[ast.Node] = []
    temp = None
    for token in tokens:
        if isinstance(token, ast.Text) and token.format_type == "normal":
            if temp is None:
                temp = token.inner_text
            else:
                temp = temp + token.inner_text  # type: ignore
                # This is a mypy bug. The statement *is* reachable
        elif check_footnotes and isinstance(token, ast.Footnote):
            if footnotes is None:
                raise ValueError(
                    "Argument 'footnotes' is required when 'check_footnotes' is True"
                )
            if footnotes[token.name] is not None:
                output.append(token)
        else:
            if temp is not None:
                output.append(ast.Text("normal", temp))
                temp = None
            output.append(token)
    return output


def unparse(tokens: ast.Document) -> str:
    """For debugging"""
    # TODO: fully implement
    output = ""
    for token in tokens.nodes:
        if isinstance(token, ast.Header):
            output += "#" * token.length + " " + token.text
        elif isinstance(token, ast.Text):
            output += (
                escapes.handle.ESCAPE_MAP[token.format_type]
                + escapes.handle[token.format_type](token.inner_text)
                + escapes.handle.ESCAPE_MAP[token.format_type]
            )
        elif isinstance(token, ast.Specdent):
            escaped = "\\:"
            output += f":{token.spec.replace(':',escaped)}:\n"
            output += textwrap.indent(token.inner_content, "    ")
        elif isinstance(token, ast.Spec):
            escaped = "\\:"
            output += f":{token.inner_text.replace(':',escaped)}:"
        elif isinstance(token, ast.Link):  # TODO: String
            output += "[" + unparse(token.inner_text) + "]"
            output += (
                f"({token.link_url}"
                + (f" {token.title!r}" if token.title else "")
                + (f" #{token.link_id}" if token.link_id else "")
                + ")"
            )
        elif token is ast.NEWLINE:
            output += "\n"
    return output


def inline_markup_document(doc: str) -> ast.InlineDocument:
    return ast.InlineDocument(
        _clean(_parse_inline_markup(doc).tokens + [ast.NEWLINE], check_footnotes=False)[
            :-1
        ]
    )


def _parse_inline_markup(doc: str) -> InlineMarkup:
    tokens: List[ast.Node] = []
    footnotes: Dict[str, Optional[ast.InlineDocument]] = {}
    for match in re.finditer(INLINE_RE, doc):
        kind = match.lastgroup
        assert kind is not None
        text = re.match(REs[kind], match.group())
        assert text is not None

        if kind == "spec":
            tokens.append(
                plugin.manager.hook.handle_spec(spec=text[1])  # pylint: disable=E1101
            )
        elif kind == "link":
            tokens.append(
                ast.Link(
                    inline_markup_document(text["link_text"].replace("\\]", "]")),
                    text["link_url"],
                    text["link_title"],
                    text["link_id"][1:] if text["link_id"] else None,
                )
            )
        elif kind == "image":
            tokens.append(
                ast.Image(
                    text["image_alt_text"].replace("\\]", "]"),
                    text["image_url"],
                    text["image_caption"],
                )
            )
        elif kind == "footnote":
            footnotes[text[1]] = None
            tokens.append(ast.Footnote(text[1]))
        else:
            tokens.append(
                ast.Text(
                    kind,
                    text[1],
                )
            )
    return InlineMarkup(tokens, footnotes)


def parse(doc: str) -> ast.Document:
    """Parse a document into AST

    Args:
        doc (str): The document to parse

    Returns:
        ast.Document: The AST representing the whole document

    """
    tokens: List[ast.Node] = []
    footnotes: Dict[str, Optional[ast.InlineDocument]] = {}

    specdent = False
    specdent_inner = ""
    specdent_spec = ""

    # list_items = []
    # in_list = False
    # indent = 0

    for line in doc.splitlines():
        if specdent:
            if line.startswith("    ") or line.startswith("\t"):
                specdent_inner += line + "\n"
                continue
            # end
            if specdent_inner:  # Has content
                tokens.append(
                    plugin.manager.hook.handle_specdent(  # pylint: disable=E1101
                        spec=specdent_spec, inner_text=specdent_inner
                    )
                )
                specdent = False
                specdent_inner = ""
                specdent_spec = ""
            else:
                tokens.append(
                    plugin.manager.hook.handle_spec(  # pylint: disable=E1101
                        spec=specdent_spec
                    )
                )
                tokens.append(ast.NEWLINE)

                inline_markup = _parse_inline_markup(line)
                tokens.extend(inline_markup.tokens)
                tokens.append(ast.NEWLINE)
                footnotes.update(inline_markup.footnotes)

                specdent = False
                specdent_inner = ""
                specdent_spec = ""
                continue
        match = SPECDENT_START.match(line)
        if match:
            specdent = True
            specdent_spec = match[1]
            continue

        match = HEADER_RE.match(line)
        if match:
            tokens.append(ast.Header(len(match[1]), match[2]))

        match = FOOTNOTE_CONTENT.match(line)
        if match:
            print(match)
            footnotes.update({match[1]: inline_markup_document(match[2])})

        match = LIST_RE.match(line)
        if match:
            ...
        else:
            inline_markup = _parse_inline_markup(line)
            tokens.extend(inline_markup.tokens)
            footnotes.update({**inline_markup.footnotes, **footnotes})
        tokens.append(ast.NEWLINE)

    if specdent_inner:  # Has content
        tokens.append(
            plugin.manager.hook.handle_specdent(  # pylint: disable=E1101
                spec=specdent_spec, inner_text=specdent_inner
            )
        )
    tokens = _clean(tokens, footnotes=footnotes)
    output = ast.Document(tokens)
    output.footnotes = {k: v for k, v in footnotes.items() if v is not None}

    return output
