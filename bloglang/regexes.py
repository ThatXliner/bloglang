"""Buncha regexes for helping the parser"""
import re

# _STRING_RE = r"(\".*?(?<!\\)(?:\\\\)*?\"|'.*?(?<!\\)(?:\\\\)*?')"

HEADER_RE = re.compile(r"^(#{1,6})\s*(.+)$", flags=re.MULTILINE)
LIST_RE = re.compile(r"^(?P<indent> *)-\s*(?P<text>.+)$", flags=re.MULTILINE)

CODE = "code", r"`(.+?)(?<!\\)(?:\\\\)*?`"
ITALIC = "italic", r"\*(?!\*\*?)(.+?)(?<!\\)(?:\\\\)*?\*"
BOLD = "bold", r"\*\*(?!\*)(.+?)(?<!\\)(?:\\\\)*?\*\*"
BOTH = "both", r"\*\*\*(.+?)(?<!\\)(?:\\\\)*?\*\*\*"
UNDERLINE = "underline", r"__(.*?)(?<!\\)(?:\\\\)*?__"
STRIKETHROUGH = "strikethrough", r"~~(.*?)(?<!\\)(?:\\\\)*?~~"

FOOTNOTE = "footnote", r"\[\s*\^\s*(.+?)(?<!\\)(?:\\\\)*?\](?!\s*\()"
FOOTNOTE_CONTENT = re.compile(
    r"^\s*\[\s*\^\s*(.+?)(?<!\\)(?:\\\\)*?\]\s*:\s*(.+)$", flags=re.MULTILINE
)

INLINE_SPEC = "spec", r":(.+?)(?<!\\)(?:\\\\)*?:"
LINK = (
    "link",
    r"(?!!)\[(?P<link_text>.+?)(?<!\\)(?:\\\\)*?\]\s*\(\s*(?P<link_url>[^\s]+)\s*(?P<link_title>\".*?(?<!\\)(?:\\\\)*?\"|'.*?(?<!\\)(?:\\\\)*?')?\s*(?P<link_id>#[\-\w]+)?\s*\)",
)
IMAGE = (
    "image",
    r"!\[(?P<image_alt_text>.*?)(?<!\\)(?:\\\\)*?\]\s*\(\s*(?P<image_url>[^\s]+)\s*(?P<image_caption>\".*?(?<!\\)(?:\\\\)*?\"|'.*?(?<!\\)(?:\\\\)*?')?\s*\)",
)

# r"""(".*?(?<!\\)(?:\\\\)*?"|'.*?(?<!\\)(?:\\\\)*?')"""
# (?<!\\)(?:\\\\)*?
SPECDENT_START = re.compile(
    "^" + INLINE_SPEC[1].replace("+", "*") + r"\s*$", flags=re.MULTILINE
)

PAIRS = (
    ITALIC,
    BOLD,
    BOTH,
    CODE,
    UNDERLINE,
    STRIKETHROUGH,
    INLINE_SPEC,
    LINK,
    IMAGE,
    FOOTNOTE,
    ("normal", r"(.)"),
)
REs = dict(PAIRS)

INLINE_RE = "|".join("(?P<%s>%s)" % pair for pair in PAIRS)
