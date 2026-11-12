"""The byline is config; the engine stays robbie."""

from pathlib import Path

from robbie import branding
from robbie.anchor import render
from robbie.config import Config, RepoConfig, SlackConfig


def cfg(tmp_path: Path, **kw) -> Config:
    return Config(
        slack=SlackConfig(owner_id="U0"),
        repos=[RepoConfig(slug="acme/app", reviewer_login="rev", bare=tmp_path)],
        state_dir=tmp_path,
        **kw,
    )


def test_default_stays_robbie(tmp_path):
    assert cfg(tmp_path).bot_name == "robbie"


def test_signature_follows_set_name():
    branding.set_name("PR Ops")
    try:
        assert branding.signature() == "🤖 **Automated pre-review by PR Ops**"
        inline = render({"severity": "nitpick", "title": "t", "body": "x"}, None)
        assert inline.endswith("<sub>🤖 automated pre-review by PR Ops</sub>")
    finally:
        branding.set_name("robbie")


def test_machine_markers_are_not_branding():
    # dedupe keys must survive any rename — they are how a re-run recognizes
    # its own prior comments
    from robbie import publish

    src = Path(publish.__file__).read_text()
    assert "robbie-review sha=" in src


def test_default_has_no_icon_and_keeps_the_emoji(tmp_path):
    # an instance that sets no bot_icon must sign exactly as it did before
    assert cfg(tmp_path).bot_icon == ""
    assert branding.icon() == ""
    assert branding.signature() == "\U0001F916 **Automated pre-review by robbie**"


def test_icon_replaces_the_emoji_on_the_top_level_signature():
    branding.set_name("Themis")
    branding.set_icon("https://example.test/themis.png")
    try:
        sig = branding.signature()
        assert sig == (
            '<img src="https://example.test/themis.png" width="48" align="middle"> '
            "**Automated pre-review by Themis**"
        )
        assert "\U0001F916" not in sig
    finally:
        branding.set_icon("")
        branding.set_name("robbie")


def test_icon_never_reaches_the_inline_sub_signature():
    # contract._strip falls back to line.startswith("<sub>"); an <img> prefix
    # here would walk past that guard, and a logo on every nitpick is noise
    branding.set_name("Themis")
    branding.set_icon("https://example.test/themis.png")
    try:
        sub = branding.signature_sub()
        assert sub.startswith("<sub>")
        assert "<img" not in sub
        inline = render({"severity": "nitpick", "title": "t", "body": "x"}, None)
        assert "<img" not in inline
    finally:
        branding.set_icon("")
        branding.set_name("robbie")
