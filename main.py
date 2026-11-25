#!/usr/bin/env python3
"""Entry program: copy the front-page image to /output/entry.png.

Standard library only. The image is rendered by render.py in this
repository; this program just places the finished file where the
grader expects it, so both runs write the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
