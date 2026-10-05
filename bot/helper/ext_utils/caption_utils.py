import re


ESCAPED = {"|": "\ue000", "{": "\ue001", "}": "\ue002"}
RESTORED = {value: key for key, value in ESCAPED.items()}
VARIABLE = re.compile(r"\{([a-z_]+)\}")


def split_template(template):
    parts = [""]
    index = 0
    while index < len(template):
        char = template[index]
        if (
            char == "\\"
            and index + 1 < len(template)
            and template[index + 1] in ESCAPED
        ):
            parts[-1] += ESCAPED[template[index + 1]]
            index += 2
        elif char == "|":
            parts.append("")
            index += 1
        else:
            parts[-1] += char
            index += 1
    return parts


def fields(template):
    return {
        field
        for part in split_template(template)
        for field in VARIABLE.findall(part)
    }


def render(template, values):
    def interpolate(text):
        return VARIABLE.sub(
            lambda match: str(values.get(match.group(1), match.group(0))), text
        )

    def unescape(text):
        for escaped, literal in RESTORED.items():
            text = text.replace(escaped, literal)
        return text

    parts = [interpolate(part) for part in split_template(template)]
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
