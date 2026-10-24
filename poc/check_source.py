#!/usr/bin/env python3
"""Non-invasive source checker for GHSA-994f-577q-hhph."""

from pathlib import Path
import argparse
import sys


RELATIVE_PATH = Path("system/typemill/Models/SvgSanitizer.php")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a local TypeMill tree for the SVG processing-instruction fix."
    )
    parser.add_argument("typemill_root", type=Path, help="path to a TypeMill source tree")
    args = parser.parse_args()

    source_path = args.typemill_root.resolve() / RELATIVE_PATH
    if not source_path.is_file():
        print(f"[error] file not found: {source_path}", file=sys.stderr)
        return 2

    source = source_path.read_text(encoding="utf-8", errors="replace")
    controls = {
        "network-disabled XML loading (LIBXML_NONET)": "LIBXML_NONET" in source,
        "DOCTYPE rejection": "->doctype" in source,
        "processing-instruction node handling": "XML_PI_NODE" in source,
        "central PI/comment removal routine": "removeProcessingInstructionsAndComments" in source,
    }

    print(f"TypeMill SVG sanitizer: {source_path}")
    for label, present in controls.items():
        print(f"[{'present' if present else 'missing'}] {label}")

    if all(controls.values()):
        print("Result: the controls used by the 2.27.0 fix are present.")
        return 0

    print(
        "Result: one or more 2.27.0 security controls are absent; "
        "this source matches the vulnerable sanitizer pattern."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
