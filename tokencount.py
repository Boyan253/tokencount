#!/usr/bin/env python3
"""Estimate how many LLM tokens a pile of text is, and what it would cost."""

import argparse
import os
import re
import sys

__version__ = "0.1.0"

# A BPE tokenizer splits on word boundaries, punctuation and whitespace runs.
# Counting those pieces lands within a few percent of real tokenizers on
# ordinary prose and code, with no model files to download.
PIECES = re.compile(r"\w+|[^\w\s]|\s+")


def estimate(text):
    """Approximate the token count of a string."""
    total = 0
    for piece in PIECES.findall(text):
        if piece.isspace():
            total += piece.count("\n")
            continue
        if piece.isalnum():
            # long words split into multiple subword tokens, roughly every 4 chars
            total += max(1, (len(piece) + 3) // 4)
        else:
            total += 1
    return total


def cost(tokens, price_per_million):
    return tokens / 1_000_000 * price_per_million


def human(number):
    for unit, size in (("M", 1_000_000), ("k", 1_000)):
        if number >= size:
            return "%.1f%s" % (number / size, unit)
    return str(number)


def read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("files", nargs="*", default=["-"],
                    help="files to measure, or nothing for stdin")
    ap.add_argument("--price", type=float, default=0.0,
                    help="input price per million tokens, e.g. 3.00")
    ap.add_argument("--limit", type=int, default=0,
                    help="warn when the total exceeds this many tokens")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print the total")
    args = ap.parse_args(argv)

    paths = args.files or ["-"]
    total = 0
    rows = []
    for path in paths:
        try:
            text = read(path)
        except OSError as exc:
            print("tokencount: %s" % exc, file=sys.stderr)
            continue
        tokens = estimate(text)
        total += tokens
        rows.append((path, len(text), tokens))

    if not args.quiet:
        for path, chars, tokens in sorted(rows, key=lambda r: -r[2]):
            name = path if path == "-" else os.path.relpath(path)
            print("%9s tokens  %9s chars  %s" % (human(tokens), human(chars), name))
        if len(rows) > 1:
            print("-" * 40)
    print("%9s tokens total" % human(total))
    if args.price:
        print("%9.4f USD at $%.2f per million" % (cost(total, args.price), args.price))
    if args.limit and total > args.limit:
        print("over the %s token limit" % human(args.limit), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
