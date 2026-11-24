#!/usr/bin/env python3
"""One Word for the Boss — writes exactly one word to entry.txt.

The word: "Buzzwordsmith" — the boss whose every sentence is
synergy, circle back, leverage, bandwidth. One word, no spaces,
no trailing newline, so the gate sees exactly what the judge sees.
"""

import os
import sys

WORD = "Buzzwordsmith"


def main():
    # Validate before writing anything: exactly one word, 1-30 chars.
    if not WORD or len(WORD) > 30:
        sys.stderr.write("word must be 1-30 characters\n")
        return 1
    if WORD != WORD.strip() or any(ch.isspace() for ch in WORD):
        sys.stderr.write("word must be a single word with no whitespace\n")
        return 1

    data = WORD.encode("utf-8")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path = os.path.join(out_dir, "entry.txt")

    os.umask(0o022)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        try:
            os.write(fd, data)
        finally:
            os.close(fd)
    except OSError:
        # Fallback only if the primary output dir is unavailable.
        fallback = os.path.join("output", "entry.txt")
        os.makedirs("output", exist_ok=True)
        fd = os.open(fallback, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        try:
            os.write(fd, data)
        finally:
            os.close(fd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
