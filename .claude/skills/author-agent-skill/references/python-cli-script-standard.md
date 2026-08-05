# Stdlib-Only Python CLI Script Standard

> Every executable CLI script under this project that depends only on the Python standard library follows this standard. The goal is for such scripts to be callable directly from the command line by an agent or a human, importable for unit testing, and structurally obvious at a glance.

---

## 1. Scope

Applies to command-line scripts that depend only on the Python stdlib and pull in no third-party packages. These scripts perform deterministic, mechanical work (creating directories, validation, aggregation, etc.) and are invoked from the command line by a higher-level skill or agent.

---

## 2. Two-Layer Function Structure

Every script has at least two fixed functions. The lower-level `_main` carries the core logic; the top-level `main` handles command-line parsing. Responsibilities are cleanly split: `_main` doesn't care what the command line looks like, and `main` doesn't care how the business logic works. Finer-grained logic can be broken out into further module-level helper functions, but these two layers are the fixed skeleton.

---

## 3. The Core Function `_main`

`_main` takes already-parsed, type-annotated parameters, e.g. `def _main(target: Path, quiet: bool = False) -> int`.

The script's main docstring lives here, explaining what the script actually does. The core logic, along with side effects like reading/writing files or printing results, all belong here. The function returns an `int` as the exit code.

Because its inputs are clean, typed values with no command-line details mixed in, tests can `import` it and call `_main(...)` directly, without going through the command line.

---

## 4. The Top-Level Parsing Function `main`

`main` has the signature `def main(argv: list[str] | None = None) -> int`. It uses argparse to parse arguments from `sys.argv`, turns the command line into correct key-value pairs, then calls `_main` with keyword arguments and returns `_main`'s result unchanged.

`argv` defaults to `None`, so argparse reads from `sys.argv`; passing an explicit list makes it easy to simulate a command line in tests. `main` itself contains no business logic — only argument parsing and dispatch.

---

## 5. Always Use `--arg_name` Keyword Style

All arguments use the explicit `--arg_name` keyword style; no positional arguments. Flag names match `_main`'s parameter names exactly, both using underscores, so the mapping from command line to function arguments is obvious at a glance.

Required inputs use `required=True`. Boolean switches use `action="store_true"`. Optional values get a `default`. Every argument has a `help` string.

---

## 6. Entry Point and Exit Codes

The end of the file always has this line:

```python
if __name__ == "__main__":
    sys.exit(main())
```

Exit code semantics are consistent: `0` for success, `1` for a runtime failure (a business-level error), `2` for a usage error (returned automatically by argparse when arguments are invalid).

---

## 7. Other Conventions

Add `from __future__ import annotations` at the top of the file, and give every function complete type hints.

Use only the standard library; pull in no third-party dependencies.

Docstrings and error messages are written in English, since these scripts are meant for machines and to run across environments. Error messages go to stderr; normal output goes to stdout.

---

## 8. Skeleton Example

```python
#!/usr/bin/env python3
"""One line module summary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _main(target: Path, quiet: bool = False) -> int:
    """Do the real work. The main docstring and core logic live here.

    Returns an exit code: 0 on success, 1 on failure.
    """
    if not target.exists():
        print(f"ERROR: {target} not found", file=sys.stderr)
        return 1
    if not quiet:
        print(f"Processing {target}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="example_tool",
        description="One line description of the tool.",
    )
    parser.add_argument("--target", type=Path, required=True, help="path to process")
    parser.add_argument("--quiet", action="store_true", help="suppress normal output")
    args = parser.parse_args(argv)
    return _main(target=args.target, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
```
