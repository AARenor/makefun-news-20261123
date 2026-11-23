#!/usr/bin/env python3
"""Write the 23 November 2026 news image to the output directory.

The finished 1024x1024 PNG ships next to this file as entry.png and is
copied as is, so a run needs no network and no imaging library. The
destination is $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when
that variable is unset.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

SOURCE_IMAGE = Path(__file__).resolve().parent / "entry.png"


def main() -> Path:
    """Copy entry.png into the output directory and return its path."""
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output") / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_IMAGE, target)
    return target


if __name__ == "__main__":
    print(main())
