"""Helpers for rendering per-user Telegram leech caption templates."""

import re


_ESCAPED = {"|": "\ue000", "{": "\ue001", "}": "\ue002"}
_RESTORE_ESCAPED = {value: key for key, value in _ESCAPED.items()}
_VARIABLE = re.compile(r"\{([a-z_]+)\}")


def _split_template(template):
    """Split a template on unescaped pipes while preserving escaped literals."""
    parts = [""]
    index = 0
    while index < len(template):
        char = template[index]
        if (
            char == "\\"
            and index + 1 < len(template)
            and template[index + 1] in _ESCAPED
        ):
            parts[-1] += _ESCAPED[template[index + 1]]
            index += 2
        elif char == "|":
            parts.append("")
            index += 1
        else:
            parts[-1] += char
            index += 1
    return parts


def caption_template_fields(template):
    """Return the placeholder names used in a template, excluding escaped ones."""
    return {
        field
        for part in _split_template(template)
        for field in _VARIABLE.findall(part)
    }


def render_caption_template(template, values):
    """Render placeholders, then apply each ``|find:replace`` patch in order."""

    def interpolate(text):
        return _VARIABLE.sub(
            lambda match: str(values.get(match.group(1), match.group(0))), text
        )

    def unescape(text):
        for escaped, literal in _RESTORE_ESCAPED.items():
            text = text.replace(escaped, literal)
        return text

    parts = [interpolate(part) for part in _split_template(template)]
    result = unescape(parts[0])
    for patch in parts[1:]:
        if ":" not in patch:
            continue
        find, replace = patch.split(":", 1)
        find = unescape(interpolate(find))
        replace = unescape(interpolate(replace))
        if find:
            result = result.replace(find, replace)
    return result
