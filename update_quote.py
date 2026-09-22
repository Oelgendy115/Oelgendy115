#!/usr/bin/env python3
"""Rotate the book quote between the BOOK_QUOTE markers in README.md."""

import random
import sys
from pathlib import Path

README_PATH = Path(__file__).with_name("README.md")
QUOTES_PATH = Path(__file__).with_name("quotes.txt")

START_MARKER = "<!-- BOOK_QUOTE_START -->"
END_MARKER = "<!-- BOOK_QUOTE_END -->"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_quotes(path):
    quotes = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        fields = [field.strip() for field in line.split("|")]
        if len(fields) != 3 or not all(fields):
            print(f"warning: skipping malformed line {lineno}", file=sys.stderr)
            continue
        quotes.append(tuple(fields))
    return quotes


def render(quote, book, author):
    return f"> “{quote}”\n>\n> — *{book}*, {author}"


def main():
    if not README_PATH.is_file():
        fail(f"{README_PATH.name} not found")
    if not QUOTES_PATH.is_file():
        fail(f"{QUOTES_PATH.name} not found")

    readme = README_PATH.read_text(encoding="utf-8")

    start = readme.find(START_MARKER)
    if start == -1:
        fail(f"{START_MARKER} not found in {README_PATH.name}")
    body_start = start + len(START_MARKER)
    end = readme.find(END_MARKER, body_start)
    if end == -1:
        fail(f"{END_MARKER} not found after {START_MARKER} in {README_PATH.name}")

    quotes = load_quotes(QUOTES_PATH)
    if not quotes:
        fail(f"no valid quotes found in {QUOTES_PATH.name}")

    current = readme[body_start:end].strip()
    candidates = [q for q in quotes if render(*q) != current] or quotes
    selected = random.choice(candidates)

    README_PATH.write_text(
        readme[:body_start] + "\n" + render(*selected) + "\n" + readme[end:],
        encoding="utf-8",
    )
    print(f"updated quote: {selected[0]} — {selected[1]}, {selected[2]}")


if __name__ == "__main__":
    main()
