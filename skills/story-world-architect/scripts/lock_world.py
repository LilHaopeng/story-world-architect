#!/usr/bin/env python3
"""Create an immutable-by-convention worldbuilding snapshot with SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


VERSION_RE = re.compile(r"^v\d+\.\d+(?:\.\d+)?(?:[-+][A-Za-z0-9._-]+)?$")


def safe_root(raw: str) -> Path:
    root = Path(raw).expanduser().resolve()
    if root.parent == root:
        raise ValueError("Refusing to lock a filesystem root.")
    return root


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def selected_files(root: Path) -> list[Path]:
    world = root / "设定" / "世界观"
    selected = [path for path in world.glob("*.md") if path.is_file()]
    for folder in (world / "研究", world / "模拟"):
        if folder.exists():
            selected.extend(path for path in folder.rglob("*.md") if path.is_file())
    return sorted(set(selected), key=lambda path: path.relative_to(root).as_posix())


def append_lock_log(root: Path, version: str, note: str, file_count: int) -> None:
    log = root / "设定" / "世界观" / "世界观变更.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    if not log.exists():
        log.write_text("# 世界观变更记录\n", encoding="utf-8")
    stamp = datetime.now(timezone.utc).isoformat()
    entry = (
        f"\n## LOCK {version}\n\n"
        f"- 时间：{stamp}\n"
        f"- 文件数：{file_count}\n"
        f"- 说明：{note or '无'}\n"
        f"- 快照：设定/世界观/版本/{version}/manifest.json\n"
    )
    with log.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)


def main() -> int:
    parser = argparse.ArgumentParser(description="Lock a validated worldbuilding snapshot.")
    parser.add_argument("--root", required=True, help="Fiction project root")
    parser.add_argument("--version", required=True, help="Version such as v1.0")
    parser.add_argument("--note", default="", help="Human-readable lock note")
    args = parser.parse_args()

    try:
        root = safe_root(args.root)
    except ValueError as exc:
        parser.error(str(exc))
    if not VERSION_RE.fullmatch(args.version):
        parser.error("--version must look like v1.0, v1.1.0, or v2.0-beta.")

    validator = Path(__file__).with_name("validate_world.py")
    validation = subprocess.run(
        [sys.executable, str(validator), "--root", str(root), "--scope", "handoff", "--strict"],
        check=False,
    )
    if validation.returncode != 0:
        print("Lock aborted: strict validation failed.", file=sys.stderr)
        return validation.returncode

    files = selected_files(root)
    if not files:
        print("Lock aborted: no worldbuilding files selected.", file=sys.stderr)
        return 2

    versions = root / "设定" / "世界观" / "版本"
    versions.mkdir(parents=True, exist_ok=True)
    destination = versions / args.version
    if destination.exists():
        print(f"Lock aborted: version already exists: {destination}", file=sys.stderr)
        return 2

    temp_path = Path(tempfile.mkdtemp(prefix=f".{args.version}-", dir=str(versions)))
    try:
        snapshot = temp_path / "snapshot"
        manifest_files: list[dict[str, str | int]] = []
        for source in files:
            relative = source.relative_to(root)
            target = snapshot / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            source_hash = sha256(source)
            copied_hash = sha256(target)
            if source_hash != copied_hash:
                raise OSError(f"Hash mismatch while copying {relative}")
            manifest_files.append(
                {"path": relative.as_posix(), "sha256": source_hash, "bytes": source.stat().st_size}
            )

        manifest = {
            "schema_version": 1,
            "version": args.version,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "note": args.note,
            "files": manifest_files,
        }
        (temp_path / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temp_path, destination)
    except Exception:
        if temp_path.exists() and temp_path.parent == versions and temp_path.name.startswith(f".{args.version}-"):
            shutil.rmtree(temp_path)
        raise

    append_lock_log(root, args.version, args.note, len(files))
    print(f"locked={destination}")
    print(f"files={len(files)}")
    print(f"manifest={destination / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
