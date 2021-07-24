"""AST nodes and components"""
from typing import Dict, List, Optional, Type, Union

import attr

from bloglang import escapes

# pylint: disable=too-few-public-methods,C0115


class _Node:
    pass


@attr.s(auto_attribs=True)
class Header(_Node):
    length: int = attr.ib()
    text: str

    @length.validator
    def validator_langth(self, _, value: int):  # type: ignore # pylint: disable=R0201
        if not isinstance(value, int):
            raise TypeError("'length' must be an integer")
        if not 1 <= value <= 6:
            raise ValueError("Header length must be between 1 and 6, inclusive")


@attr.s(auto_attribs=True, auto_detect=True)
class Text(_Node):
    format_type: str
    inner_text: str

    def __init__(self, format_type: str, inner_text: str) -> None:
        self.__attrs_init__(format_type, escapes.handle[format_type](inner_text))  # type: ignore # pylint: disable=E1101


def escape_spec(string: str) -> str:
    return string.replace("\\:", ":")


@attr.s(auto_attribs=True)
class Spec(_Node):
    """Inline :specs:

    NOTE: These are different from Specdents
    """

    inner_text: str = attr.ib(converter=escape_spec)


@attr.s(auto_attribs=True)
class Specdent(_Node):
    spec: str = attr.ib(converter=escape_spec)
    inner_content: str


@attr.s(auto_attribs=True)
class Comment(_Node):
    text: str


class Singleton(type):
    """Freshly stolen singleton implementation from StackOverflow.

    https://stackoverflow.com/q/6760685
    """

    _instances = {}  # type: ignore

    def __repr__(cls) -> str:
        return "<" + cls.__name__ + ">"

    def __call__(cls, *args, **kwargs):  # type: ignore
        if cls not in cls._instances:  # type: ignore
            cls._instances[cls] = super().__call__(*args, **kwargs)  # type: ignore
        return cls._instances[cls]  # type: ignore


class NEWLINE(_Node, metaclass=Singleton):
    pass


Node = Union[Type[NEWLINE], _Node]


@attr.s(auto_attribs=True)
class InlineDocument(_Node):
    nodes: List[Node]


@attr.s(auto_attribs=True)
class Document:
    nodes: List[Node]
    footnotes: Dict[str, InlineDocument] = {}


def escape_str(string: Optional[str]) -> Optional[str]:
    if string is not None:
        if string[0] not in {"'", '"'}:
            raise ValueError("Invalid string")
        return string[1:-1].replace("\\" + string[0], string[0])
    return string


@attr.s(auto_attribs=True)
class Link(_Node):
    inner_text: InlineDocument
    link_url: str
    title: Optional[str] = attr.ib(converter=escape_str)
    link_id: Optional[str] = None


@attr.s(auto_attribs=True)
class Image(_Node):
    alt_text: str
    image_url: str
    caption: Optional[str] = attr.ib(converter=escape_str)


@attr.s(auto_attribs=True)
class Footnote(_Node):
    name: str


@attr.s(auto_attribs=True)
class FootnoteContent(_Node):
    name: str
    content: InlineDocument


#
# @attr.s(auto_attribs=True)
# class ListBlock(_Node):
#     items: List["ListItem"] = []
#
#
# @attr.s(auto_attribs=True)
# class ListItem(_Node):
#     text: InlineDocument
#     inner_items: "ListBlock" = ListBlock()
#
#     def add_inner_item(self, item: "ListItem"):
#         self.inner_items.items.append(item)
