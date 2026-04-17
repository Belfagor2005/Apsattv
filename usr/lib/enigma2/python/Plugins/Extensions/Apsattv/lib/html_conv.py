import re
import sys
import html.entities

text_type = str
binary_type = bytes
MAXSIZE = sys.maxsize

_UNICODE_MAP = {
    k: chr(v) for k, v in html.entities.name2codepoint.items()
}
_ESCAPE_RE = re.compile("[&<>\"']")
_UNESCAPE_RE = re.compile(r"&\s*(#?)(\w+?)\s*;")
_ESCAPE_DICT = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&apos;",
}


def ensure_str(s, encoding="utf-8", errors="strict"):
    """Coerce *s* to str (Python 3).

    - If already str, return as is.
    - If bytes, decode using given encoding.
    """
    if isinstance(s, str):
        return s
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    raise TypeError(f"not expecting type '{type(s).__name__}'")


def html_escape(value):
    return _ESCAPE_RE.sub(
        lambda match: _ESCAPE_DICT[match.group(0)], ensure_str(value).strip()
    )


def html_unescape(value):
    return _UNESCAPE_RE.sub(_convert_entity, ensure_str(value).strip())


def _convert_entity(m):
    if m.group(1) == "#":
        try:
            if m.group(2)[:1].lower() == "x":
                return chr(int(m.group(2)[1:], 16))
            else:
                return chr(int(m.group(2)))
        except ValueError:
            return f"&#{m.group(2)};"
    return _UNICODE_MAP.get(m.group(2), f"&{m.group(2)};")
