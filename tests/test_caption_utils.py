from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from pytest import raises


MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "bot"
    / "helper"
    / "ext_utils"
    / "caption_utils.py"
)
SPEC = spec_from_file_location("caption_utils", MODULE_PATH)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
render = MODULE.render


def test_case_insensitive_fields_and_ordered_patches():
    template = "<b>{FILENAME}</b> - {SIZE}|movie:film|film:video"

    assert render(template, {"filename": "movie.mkv", "size": "1GB"}) == (
        "<b>video.mkv</b> - 1GB"
    )


def test_escaped_characters_and_space():
    template = r"Literal \| and \{filename\}\s{filename}"

    assert render(template, {"filename": "movie.mkv"}) == (
        "Literal | and {filename} movie.mkv"
    )


def test_patch_count():
    template = "one one one|one:two:2"

    assert render(template, {}) == "two two one"


def test_patch_is_not_formatted():
    template = "{filename}|{filename}:renamed"

    assert render(template, {"filename": "movie.mkv"}) == "movie.mkv"


def test_unknown_field():
    with raises(KeyError):
        render("{unknown}", {})
