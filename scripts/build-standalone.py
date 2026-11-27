#!/usr/bin/env python3
"""Build standalone-demo.html from demo.html, the runtime and the sprites.

standalone-demo.html is demo.html with companion.css and companion.js inlined
and every sprite passed in as a base64 data URL, so it opens straight from
disk with no server. Never edit it by hand: change the sources, then rebuild.

Usage:
  python3 scripts/build-standalone.py           # rewrite standalone-demo.html
  python3 scripts/build-standalone.py --check   # exit 1 if it is out of date

Standard library only.
"""
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "standalone-demo.html"
# Order as in the original file, so a rebuild of unchanged sources is byte-identical.
MOODS = ["recharging", "celebrating", "coding", "idle", "sleeping", "thinking"]
CSS_TAG = '<link rel="stylesheet" href="companion.css">'
JS_TAG = '<script src="companion.js"></script>'


def build() -> str:
    demo = (ROOT / "demo.html").read_text()
    css = (ROOT / "companion.css").read_text()
    js = (ROOT / "companion.js").read_text()
    for tag in (CSS_TAG, JS_TAG):
        if demo.count(tag) != 1:
            sys.exit(f"demo.html must contain exactly one {tag}")
    sprites = {
        mood: "data:image/png;base64,"
        + base64.b64encode((ROOT / "sprites" / f"{mood}.png").read_bytes()).decode()
        for mood in MOODS
    }
    options = "<script>window.demoOptions={sprites:" + json.dumps(sprites) + "};</script>"
    return demo.replace(CSS_TAG, "<style>" + css + "</style>").replace(
        JS_TAG, "<script>" + js + "</script>" + options
    )


def main() -> int:
    html = build()
    if "--check" in sys.argv[1:]:
        if OUTPUT.read_text() == html:
            print("OK standalone-demo.html is up to date")
            return 0
        print("FAIL standalone-demo.html is out of date: run python3 scripts/build-standalone.py")
        return 1
    OUTPUT.write_text(html)
    print(f"Wrote {OUTPUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
