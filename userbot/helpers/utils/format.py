import datetime
import re

import requests
from telethon.tl.tlobject import TLObject
from telethon.tl.types import MessageEntityPre
from telethon.utils import add_surrogate

from ..functions import utc_to_local


def paste_text(text):
    asciich = ["**", "`", "__"]
    for i in asciich:
        text = re.sub(rf"\{i}", "", text)
    try:
        nekokey = (
            requests.post("https://nekobin.com/api/documents", json={"content": text})
            .json()
            .get("result")
            .get("key")
        )
        link = f"https://nekobin.com/{nekokey}"
    except Exception:
        url = "https://del.dog/documents"
        r = requests.post(url, data=text).json()
        link = f"https://del.dog/{r['key']}"
        if r["isUrl"]:
            link = f"https://del.dog/v/{r['key']}"
    return link


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


def htmlmentionuser(name, userid):
    return f"<a href='tg://user?id={userid}'>{name}</a>"


# kanged from uniborg @spechide
# https://github.com/SpEcHiDe/UniBorg/blob/d8b852ee9c29315a53fb27055e54df90d0197f0b/uniborg/utils.py#L250


def reformattext(text):
    return text.replace("~", "").replace("_", "").replace("*", "").replace("`", "")


def replacetext(text):
    return (
        text.replace(
            '"',
            "",
        )
        .replace(
            "\\r",
            "",
        )
        .replace(
            "\\n",
            "",
        )
        .replace(
            "\\",
            "",
        )
    )


def parse_pre(text):
    text = text.strip()
    return (
        text,
        [MessageEntityPre(offset=0, length=len(add_surrogate(text)), language="")],
    )


def yaml_format(obj, indent=0, max_str_len=256, max_byte_len=64):
    """
    Pretty formats the given object as a YAML string which is returned.
    (based on TLObject.pretty_format)
    """
    result = []
    if isinstance(obj, TLObject):
        obj = obj.to_dict()

    if isinstance(obj, dict):
        if not obj:
            return "dict:"
        items = obj.items()
        has_items = len(items) > 1
        has_multiple_items = len(items) > 2
        result.append(obj.get("_", "dict") + (":" if has_items else ""))
        if has_multiple_items:
            result.append("\n")
            indent += 2
        for k, v in items:
            if k == "_" or v is None:
                continue
            formatted = yaml_format(v, indent)
            if not formatted.strip():
                continue
            result.append(" " * (indent if has_multiple_items else 1))
            result.append(f"{k}:")
            if not formatted[0].isspace():
                result.append(" ")
            result.append(f"{formatted}")
            result.append("\n")
        if has_items:
            result.pop()
        if has_multiple_items:
            indent -= 2
    elif isinstance(obj, str):
        # truncate long strings and display elipsis
        result = repr(obj[:max_str_len])
        if len(obj) > max_str_len:
            result += "…"
        return result
    elif isinstance(obj, bytes):
        # repr() bytes if it's printable, hex like "FF EE BB" otherwise
        if all(0x20 <= c < 0x7F for c in obj):
            return repr(obj)
        return "<…>" if len(obj) > max_byte_len else " ".join(f"{b:02X}" for b in obj)
    elif isinstance(obj, datetime.datetime):
        # ISO-8601 without timezone offset (telethon dates are always UTC)
        return utc_to_local(obj).strftime("%Y-%m-%d %H:%M:%S")
    elif hasattr(obj, "__iter__"):
        # display iterables one after another at the base indentation level
        result.append("\n")
        indent += 2
        for x in obj:
            result.append(f"{' ' * indent}- {yaml_format(x, indent + 2)}")
            result.append("\n")
        result.pop()
        indent -= 2
    else:
        return repr(obj)

    return "".join(result)
