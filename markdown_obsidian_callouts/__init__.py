from __future__ import annotations

__version__ = "0.1.3"

import os
from pathlib import Path

def get_static_path() -> Path:
    """Return path to static assets directory."""
    return Path(__file__).parent / 'static'

def get_css_path() -> Path:
    """Return path to minified CSS file."""
    return get_static_path() / 'callouts.min.css'

def get_js_path() -> Path:
    """Return path to minified JavaScript file."""
    return get_static_path() / 'callouts.min.js'

def __getattr__(name: str):
    if name in {"CalloutsExtension", "makeExtension"}:
        from . import callouts

        return getattr(callouts, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
