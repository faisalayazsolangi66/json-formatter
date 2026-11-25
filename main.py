#!/usr/bin/env python3
"""Pretty-print, minify and validate JSON files.

Usage:
    python3 main.py data.json
    python3 main.py data.json --output pretty.json --indent 2
    python3 main.py data.json --minify --output min.json
    python3 main.py data.json --validate-only
    echo '{"a":1}' | python3 main.py -
"""
import argparse
import json
import sys


def load_json(path):
    if path == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except FileNotFoundError:
            print(f"error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        except OSError as exc:
            print(f"error: cannot read {path}: {exc}", file=sys.stderr)
            sys.exit(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)


def describe(value):
    if isinstance(value, dict):
        return f"object with {len(value)} key(s)"
    if isinstance(value, list):
        return f"array with {len(value)} item(s)"
    return f"{type(value).__name__}: {value!r}"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Pretty-print, minify and validate JSON files.")
    parser.add_argument("input", help="input JSON file, or - for stdin")
    parser.add_argument("--output", "-o", help="output file (default: stdout)")
    parser.add_argument("--minify", action="store_true",
                        help="minify instead of pretty-printing")
    parser.add_argument("--indent", type=int, default=2,
                        help="indent spaces for pretty output (default: 2)")
    parser.add_argument("--sort-keys", action="store_true",
                        help="sort object keys alphabetically")
    parser.add_argument("--validate-only", action="store_true",
                        help="only check validity, print no JSON")
    parser.add_argument("--ensure-ascii", action="store_true",
                        help="escape non-ASCII characters as \\uXXXX")
    args = parser.parse_args(argv)

    if args.indent < 0:
        parser.error("--indent must be 0 or more")

    data = load_json(args.input)

    if args.validate_only:
        print(f"Valid JSON: {describe(data)}")
        return 0

    if args.minify:
        text = json.dumps(data, sort_keys=args.sort_keys,
                          ensure_ascii=args.ensure_ascii,
                          separators=(",", ":"))
    else:
        text = json.dumps(data, sort_keys=args.sort_keys,
                          ensure_ascii=args.ensure_ascii, indent=args.indent)
    text += "\n"

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(text)
        except OSError as exc:
            print(f"error: cannot write {args.output}: {exc}", file=sys.stderr)
            return 1
        print(f"Wrote {args.output} ({len(text)} bytes)")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
