# JSON Formatter

Pretty-print, minify and validate JSON files.

## Requirements

- Python 3 (standard library only — no third-party packages)

## Usage

```bash
python3 main.py data.json
python3 main.py data.json --output pretty.json --indent 2
python3 main.py data.json --minify --output min.json
python3 main.py data.json --validate-only
echo '{"a":1}' | python3 main.py -
```

## Options

| Option | Description |
| --- | --- |
| `--output`, `-o` | Write to a file instead of stdout |
| `--minify` | Minify instead of pretty-printing |
| `--indent` | Indent spaces for pretty output (default: `2`) |
| `--sort-keys` | Sort object keys alphabetically |
| `--validate-only` | Only check validity, print no JSON |
| `--ensure-ascii` | Escape non-ASCII characters as `\uXXXX` |

## Example

```bash
$ echo '{"b": 2, "a": 1}' | python3 main.py - --sort-keys
{
  "a": 1,
  "b": 2
}
$ echo '{"b": 2, "a": 1}' | python3 main.py - --minify
{"b":2,"a":1}
```

## License

MIT — see `LICENSE`.
