#!/usr/bin/env python3
"""Export complete selected STIG authoring trees from one verified SCAP-NG r3 release.

This is preview research content, not an official publisher STIG cache and not
scanner-verified. Copies source YAML bytes unchanged and indexes Rule references.
Refs #1 #2.
"""
import argparse
import hashlib
import json
import shutil
import zipfile
from collections import deque
from pathlib import Path

import yaml

SOURCE_TAG = "v0.4.0-joval-meeting-preview-20261015-r3"
SELECTED_STIGS = {
    "rhel_9": "RHEL 9",
    "ms_windows_11": "Windows 11",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def assessment_refs(a):
    """Return explicit result refs; never infer them from titles or OVAL IDs."""
    refs = set()
    def walk(value):
        if isinstance(value, list):
            for v in value:
                walk(v)
        elif isinstance(value, dict):
            if isinstance(value.get("assessment"), str):
                refs.add(value["assessment"])
            for key, item in value.items():
                if key != "assessment":
                    walk(item)
    walk(a.get("evaluate"))
    walk(a.get("applicability"))
    for item in (a.get("dependencies") or {}).values():
        if isinstance(item, dict) and isinstance(item.get("assessment"), str):
            refs.add(item["assessment"])
    return refs


def generate(source_zip, review_manifest, output):
    archive_bytes = source_zip.read_bytes()
    review_bytes = review_manifest.read_bytes()
    review = json.loads(review_bytes)
    expected = [
        item.get("sha256") for item in review.get("archives", [])
        if item.get("file") == source_zip.name
    ]
    if len(expected) != 1 or expected[0] != digest(archive_bytes):
        raise ValueError("Unverified pinned r3 authoring archive")
    docs, source = {}, {}
    with zipfile.ZipFile(source_zip) as zip_file:
        damaged = zip_file.testzip()
        if damaged:
            raise ValueError("Damaged archive member: " + damaged)
        for name in zip_file.namelist():
            if not name.startswith("authoring/") or not name.endswith((".yaml", ".yml")):
                continue
            if Path(name).is_absolute() or ".." in Path(name).parts:
                raise ValueError("Unsafe source path: " + name)
            raw = zip_file.read(name)
            obj = yaml.safe_load(raw)
            if not isinstance(obj, dict):
                raise ValueError("Invalid native authoring document: " + name)
            docs[name], source[name] = obj, raw

    by_assessment = {}
    for path, obj in docs.items():
        a = obj.get("assessment")
        if not isinstance(a, dict):
            continue
        ident = a.get("id")
        if not isinstance(ident, str) or not ident:
            raise ValueError("Assessment identity missing: " + path)
        if ident in by_assessment:
            raise ValueError("Ambiguous Assessment identity: " + ident)
        by_assessment[ident] = path

    files, indexes, dependency_queue = set(), {}, deque()
    for folder, label in SELECTED_STIGS.items():
        prefix = f"authoring/{folder}/"
        rule_sources = sorted(
            p for p, obj in docs.items()
            if p.startswith(prefix) and "/rules/" in p and isinstance(obj.get("rule"), dict)
        )
        if not rule_sources:
            raise ValueError("Selected complete STIG has no Rule source: " + folder)
        rows = []
        seen_ids = set()
        for path in rule_sources:
            r = docs[path]["rule"]
            rid = r.get("id")
            if not isinstance(rid, str) or not rid or rid in seen_ids:
                raise ValueError("Duplicate or absent Rule ID in " + path)
            seen_ids.add(rid)
            files.add(path)
            choices = r.get("assessment_choices") or {}
            if not isinstance(choices, dict):
                raise ValueError("Invalid Assessment choices in " + path)
            direct = {}
            for kind, choice in choices.items():
                if not isinstance(choice, dict) or not isinstance(choice.get("assessment"), str):
                    continue
                ident = choice["assessment"]
                target = by_assessment.get(ident)
                direct[kind] = {
                    "id": ident,
                    "path": "complete-stigs/" + target if target else None,
                    "loaded": bool(target)
                }
                if target:
                    dependency_queue.append(ident)
            rows.append({
                "id": rid,
                "title": str(r.get("title") or rid),
                "version": str(r.get("version") or ""),
                "severity": str(r.get("severity") or "unknown"),
                "rule_path": "complete-stigs/" + path,
                "sha256": digest(source[path]),
                "assessment_choices": direct
            })
        indexes[folder] = {
            "format": "scap-ng-editor-stig-index/1",
            "stig_id": folder,
            "display_name": label,
            "source_tag": SOURCE_TAG,
            "rule_count": len(rows),
            "rules": rows
        }

    unresolved = set()
    visited = set()
    while dependency_queue:
        ident = dependency_queue.popleft()
        if ident in visited:
            continue
        visited.add(ident)
        path = by_assessment.get(ident)
        if not path:
            unresolved.add(ident)
            continue
        files.add(path)
        for dep in assessment_refs(docs[path]["assessment"]):
            dependency_queue.append(dep)

    if output.exists():
        shutil.rmtree(output)
    (output / "authoring").mkdir(parents=True)
    for path in sorted(files):
        target = output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source[path])
    for folder, index in indexes.items():
        target = output / folder / "index.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(index, indent=2) + "\n")
    catalog = {
        "format": "scap-ng-editor-complete-stigs/1",
        "classification": "preview_authoring_not_authoritative_disastig_or_scanner_results",
        "source_repository": "vanderpol/scap-ng",
        "source_tag": SOURCE_TAG,
        "source_asset": source_zip.name,
        "source_sha256": digest(archive_bytes),
        "review_manifest_sha256": digest(review_bytes),
        "description": "Two complete, selected STIG Rule sets from a pinned SCAP-NG r3 six-STIG research authoring release.",
        "stig_count": len(indexes),
        "rule_count": sum(i["rule_count"] for i in indexes.values()),
        "assessment_count": len([p for p in files if "assessment" in docs[p]]),
        "unresolved_assessment_refs": sorted(unresolved),
        "stigs": [
            {
                "id": folder,
                "name": SELECTED_STIGS[folder],
                "rule_count": index["rule_count"],
                "index_path": f"complete-stigs/{folder}/index.json"
            }
            for folder, index in sorted(indexes.items())
        ]
    }
    (output / "manifest.json").write_text(json.dumps(catalog, indent=2) + "\n")
    if unresolved:
        raise ValueError("Incomplete assessment closure: " + ", ".join(sorted(unresolved)[:12]))
    return catalog


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-zip", type=Path, required=True)
    parser.add_argument("--review-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("complete-stigs"))
    args = parser.parse_args()
    manifest = generate(args.source_zip, args.review_manifest, args.output)
    print(json.dumps({"stigs": manifest["stig_count"], "rules": manifest["rule_count"],
                      "assessments": manifest["assessment_count"]}))


if __name__ == "__main__":
    main()
