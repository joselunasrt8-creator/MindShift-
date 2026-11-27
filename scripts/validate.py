#!/usr/bin/env python3
"""Run MindShift's deterministic, model-free research artifact validation."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FREEZE_COMMIT = "56886b7bb7018d729dc4a65651c7e635878dc697"
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LOCAL_REF = re.compile(r"""(?:src|href)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION BLOCKED: {message}")


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def read_json(relative: str) -> dict:
    try:
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read {relative}: {exc}")


def required_commits() -> set[str]:
    commits = {
        read_json("docs/issue-81/source-manifest.json")["source_commit"],
        read_json("docs/issue-81/v2/source-manifest.json")["source_commit"],
        FREEZE_COMMIT,
    }
    cohort = read_json("docs/issue-91/assessment-input/cohort.json")
    commits.update(entry["commit"] for entry in cohort["evidence"])
    return commits


def check_git_history() -> None:
    if sys.version_info < (3, 10):
        fail("Python 3.10 or newer is required")
    if sys.flags.optimize or os.environ.get("PYTHONOPTIMIZE") not in (None, "", "0"):
        fail("optimized Python is unsupported; run with normal Python assertions enabled")

    root_result = git("rev-parse", "--show-toplevel")
    if root_result.returncode:
        fail("run this command from a Git checkout")
    if Path(root_result.stdout.strip()).resolve() != ROOT.resolve():
        fail("Git root does not match the MindShift repository root")

    shallow = git("rev-parse", "--is-shallow-repository")
    if shallow.returncode or shallow.stdout.strip() != "false":
        fail("complete Git history is required; run: git fetch --unshallow --tags")

    missing = []
    for commit in sorted(required_commits()):
        result = git("cat-file", "-e", f"{commit}^{{commit}}")
        if result.returncode:
            missing.append(commit)
    if missing:
        fail("required historical commit objects are missing: " + ", ".join(missing))

    ancestry = git("merge-base", "--is-ancestor", FREEZE_COMMIT, "HEAD")
    if ancestry.returncode:
        fail(
            "Issue #81 v2 freeze commit is not established as an ancestor of HEAD: "
            + FREEZE_COMMIT
        )


def check_readme_references() -> None:
    readme = ROOT / "README.md"
    content = readme.read_text(encoding="utf-8")
    targets = [match.group(1).strip().split()[0].strip("<>") for match in MARKDOWN_LINK.finditer(content)]
    targets.extend(match.group(1).strip() for match in HTML_LOCAL_REF.finditer(content))

    checked = 0
    missing = []
    for target in targets:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith("#"):
            continue
        relative = unquote(parsed.path)
        if not relative:
            continue
        candidate = (ROOT / relative).resolve()
        if not candidate.is_relative_to(ROOT.resolve()):
            missing.append(f"{target} (path escapes repository)")
        elif not candidate.exists():
            missing.append(target)
        checked += 1

    if missing:
        fail("README contains missing local references: " + ", ".join(missing))

    grandmaster = ROOT / "docs/grandmaster-mode.md"
    try:
        grandmaster.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"docs/grandmaster-mode.md is not readable UTF-8 Markdown: {exc}")

    print(f"README references: PASS ({checked} local links/images; Grandmaster Mode is UTF-8)")


def run_step(label: str, *command: str) -> None:
    print(f"\n=== {label} ===", flush=True)
    result = subprocess.run(
        [sys.executable, *command],
        cwd=ROOT,
        check=False,
    )
    if result.returncode:
        fail(f"{label} failed with exit code {result.returncode}")


def main() -> None:
    check_git_history()
    print(
        "Git history: PASS "
        f"({len(required_commits())} required commits present; full history; "
        f"{FREEZE_COMMIT[:12]} is an ancestor of HEAD)"
    )

    run_step("Issue #81 v1 preregistration", "docs/issue-81/validate_protocol.py")
    run_step("Issue #81 v2 construction preflight", "docs/issue-81/v2/construct_and_validate.py")
    run_step("Issue #81 v2 frozen evidence", "docs/issue-81/v2/validate_evidence.py")
    run_step("Issue #91 frozen reconstruction preflight", "docs/issue-91/validate_and_reconstruct.py")
    run_step(
        "Issue #91 unit tests",
        "-m",
        "unittest",
        "discover",
        "-s",
        "docs/issue-91",
        "-p",
        "test_*.py",
        "-v",
    )
    check_readme_references()
    print("\nALL RESEARCH VALIDATIONS: PASS")


if __name__ == "__main__":
    main()
