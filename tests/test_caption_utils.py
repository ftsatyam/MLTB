from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


_MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "bot"
    / "helper"
    / "ext_utils"
    / "caption_utils.py"
)
_SPEC = spec_from_file_location("caption_utils", _MODULE_PATH)
_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
caption_template_fields = _MODULE.caption_template_fields
render_caption_template = _MODULE.render_caption_template


def test_renders_variables_and_applies_patches_in_order():
    template = "<b>{filename}</b> - {size}|movie:film|film:video"

    assert render_caption_template(
        template, {"filename": "movie.mkv", "size": "1GB"}
    ) == "<b>video.mkv</b> - 1GB"


def test_escaped_pipe_and_braces_are_literals():
    template = r"Literal \| and \{filename\}: {filename}"

    assert render_caption_template(template, {"filename": "movie.mkv"}) == (
        "Literal | and {filename}: movie.mkv"
    )


def test_fields_excludes_escaped_placeholders_and_includes_patch_fields():
    template = r"\{filename\} {size}|{filename}:renamed"

    assert caption_template_fields(template) == {"filename", "size"}


def test_unknown_variables_are_preserved_and_values_may_contain_pipes():
    template = "{unknown} {filename}"

    assert render_caption_template(
        template, {"filename": "part|one.mkv"}
    ) == "{unknown} part|one.mkv"
