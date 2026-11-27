#!/usr/bin/env python3
"""Create a deterministic companion provenance manifest for an InstrumentRunRecord.

This minimal collector does not execute research instruments and does not infer
missing measurements. It hashes a completed record file and writes a separate
manifest using MindShift's canonical JSON byte representation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="InstrumentRunRecord JSON file")
    parser.add_argument("--manifest", type=Path, help="output provenance manifest path")
    args = parser.parse_args()

    try:
        record_bytes = args.record.read_bytes()
        record = json.loads(record_bytes.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(f"cannot read valid UTF-8 JSON record: {exc}")

    if not isinstance(record, dict):
        parser.error("record must be a JSON object")

    canonical_record = canonical_bytes(record)
    manifest = {
        "manifest_version": "1.0.0",
        "record_path": args.record.as_posix(),
        "record_sha256": sha256(canonical_record),
        "record_byte_sha256": sha256(record_bytes),
        "canonicalization": "json.dumps(sort_keys=True,separators=(',',':')) + LF",
    }
    manifest["manifest_hash"] = sha256(canonical_bytes(manifest))

    output = args.manifest or args.record.with_name(args.record.stem + ".provenance.json")
    output.write_bytes(canonical_bytes(manifest))
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
