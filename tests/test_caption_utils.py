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
fields = _MODULE.fields
render = _MODULE.render


def test_render():
    template = "<b>{filename}</b> - {size}|movie:film|film:video"

    assert render(template, {"filename": "movie.mkv", "size": "1GB"}) == (
        "<b>video.mkv</b> - 1GB"
    )


def test_escape():
    template = r"Literal \| and \{filename\}: {filename}"

    assert render(template, {"filename": "movie.mkv"}) == (
        "Literal | and {filename}: movie.mkv"
    )


def test_fields():
    template = r"\{filename\} {size}|{filename}:renamed"

    assert fields(template) == {"filename", "size"}


def test_unknown_and_pipe():
    template = "{unknown} {filename}"

    assert render(template, {"filename": "part|one.mkv"}) == "{unknown} part|one.mkv"
