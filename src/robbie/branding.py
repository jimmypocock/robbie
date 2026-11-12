"""The bot's byline. The engine stays robbie; what humans read is config.

`config.load` calls `set_name` once with `bot_name` from robbie.yaml, and every
string a person sees goes through here — so two instances of the same code can
sign differently (JM's as robbie, Jimmy's as PR Ops). Machine markers
(`<!-- robbie-* -->`) are dedupe keys, not branding, and never change.

Both signature forms are functions on purpose: publish appends them and
contract._strip matches them, and those must be the same string at runtime —
a constant captured at import would freeze one side out of a rename.

`bot_icon` rides the TOP-LEVEL signature only. The inline `<sub>` form stays
text: contract._strip falls back to `line.startswith("<sub>")`, so an `<img>`
prefix there would walk straight past that guard — and a logo on every nitpick
is noise. Unset, both forms are byte-identical to what they were before the
icon existed, which is what keeps JM's instance unchanged.
"""

_NAME = "robbie"
_ICON = ""


def set_name(name: str) -> None:
    global _NAME
    _NAME = name


def set_icon(url: str) -> None:
    global _ICON
    _ICON = url


def name() -> str:
    return _NAME


def icon() -> str:
    return _ICON


def signature() -> str:
    if _ICON:
        return f'<img src="{_ICON}" width="48" align="middle"> **Automated pre-review by {_NAME}**'
    return f"🤖 **Automated pre-review by {_NAME}**"


def signature_sub() -> str:
    return f"<sub>🤖 automated pre-review by {_NAME}</sub>"
