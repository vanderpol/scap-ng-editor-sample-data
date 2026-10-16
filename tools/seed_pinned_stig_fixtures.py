#!/usr/bin/env python3
"""Seed source-backed editor smoke fixtures from the verified r3 authoring release.

Copies archived authoring bytes unchanged. Checks source digests, Rule choices,
local graph references, and transitive Assessment dependencies. This proves
fixture provenance, NOT 0.4 compilation or scanner semantics. Refs #1.
"""
import argparse
import hashlib
import json
from collections import deque
from pathlib import Path
import shutil
import zipfile

import yaml

SOURCE_TAG = "v0.4.0-joval-meeting-preview-20261015-r3"
CASES = (
    ("rhel_9", "SV-257851", "simple Linux check"),
    ("windows_11", "SV-253254", "registry State alternatives"),
    ("windows_11", "SV-253495", "user-right and nested WMI records"),
    ("rhel_9", "SV-257889", "source ObjectComponent / Variable"),
    ("apache_2_4_unix", "SV-214228", "Apache dynamic regex capture"),
    ("windows_server_dns", "SV-259345", "DNS dynamic Variables"),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def generate(source_zip, review_manifest, output, report):
    data = source_zip.read_bytes()
    review = json.loads(review_manifest.read_text())
    expected = [x.get("sha256") for x in review.get("archives", [])
                if x.get("file") == source_zip.name]
    if len(expected) != 1 or expected[0] != sha(data):
        raise ValueError("Unverified r3 source ZIP checksum")
    docs, blobs = {}, {}
    with zipfile.ZipFile(source_zip) as z:
        if z.testzip():
            raise ValueError("Corrupt release ZIP")
        for name in z.namelist():
            if not name.startswith("authoring/") or not name.endswith((".yaml", ".yml")):
                continue
            if ".." in Path(name).parts or name.startswith("/"):
                raise ValueError("Unsafe archive path " + name)
            source = z.read(name)
            parsed = yaml.safe_load(source)
            if not isinstance(parsed, dict):
                raise ValueError("Not a native mapping " + name)
            docs[name], blobs[name] = parsed, source
    by_id = {}
    for path, doc in docs.items():
        a = doc.get("assessment")
        if not isinstance(a, dict):
            continue
        ident = a.get("id")
        if not isinstance(ident, str) or not ident:
            raise ValueError("Assessment ID missing " + path)
        if ident in by_id:
            raise ValueError("Ambiguous Assessment ID " + ident)
        by_id[ident] = path

    selected, cases, todo = {}, [], deque()
    for benchmark, sv, description in CASES:
        name = f"authoring/{benchmark}/rules/{sv}.rule.yaml"
        if name not in docs:
            raise ValueError("Expected source Rule absent: " + name)
        rule = docs[name].get("rule")
        if not isinstance(rule, dict) or rule.get("id") != sv:
            raise ValueError("Rule source ID mismatch: " + name)
        choice = (rule.get("assessment_choices") or {}).get("automated")
        ident = choice.get("assessment") if isinstance(choice, dict) else None
        if ident not in by_id:
            raise ValueError("Unresolved automated Rule choice " + sv)
        target = by_id[ident]
        a = docs[target]["assessment"]
        if a.get("mode") != "automated":
            raise ValueError("Wrong Assessment mode in " + target)
        if (a.get("specification") or {}).get("version") != "0.4.0":
            raise ValueError("Not a scoped 0.4 draft Assessment: " + target)
        selected[name] = {"role": "source_rule", "cases": [sv]}
        todo.append((ident, sv))
        cases.append({"benchmark": benchmark, "rule_id": sv, "purpose": description,
                      "rule_source": name, "automated_assessment_source": target,
                      "automated_assessment_id": ident})

    while todo:
        ident, sv = todo.popleft()
        if ident not in by_id:
            raise ValueError(f"Missing Assessment dependency {ident} ({sv})")
        path = by_id[ident]
        if path in selected:
            if sv not in selected[path]["cases"]:
                selected[path]["cases"].append(sv)
            continue
        a = docs[path]["assessment"]
        selected[path] = {"role": "assessment", "cases": [sv]}
        tests = a.get("tests") or {}
        objects = a.get("shared_objects") or {}
        variables = a.get("variables") or {}
        for test_id, test in tests.items():
            if isinstance(test, dict) and isinstance(test.get("object"), str):
                if test["object"] not in objects:
                    raise ValueError(f"Unresolved Object {test['object']} at {path}:{test_id}")

        def scan_variables(node, loc):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "variable" and isinstance(value, str) and value not in variables:
                        raise ValueError(f"Unresolved Variable {value} at {path}:{loc}")
                    scan_variables(value, loc + "/" + str(key))
            elif isinstance(node, list):
                for i, value in enumerate(node):
                    scan_variables(value, loc + "/" + str(i))

        for root in ("tests", "shared_objects", "variables"):
            scan_variables(a.get(root), root)
        deps = a.get("dependencies") or {}
        if not isinstance(deps, dict):
            raise ValueError("Invalid dependencies in " + path)
        for alias, dep in deps.items():
            if not isinstance(dep, dict) or not isinstance(dep.get("assessment"), str):
                raise ValueError("Invalid Assessment dependency " + path + ":" + alias)
            todo.append((dep["assessment"], sv))

    if output.exists():
        shutil.rmtree(output)
    entries = []
    for original in sorted(selected):
        dest = output / original
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blobs[original])
        entries.append({"path": (Path("focused-fixtures/source-backed") / original).as_posix(),
                        "archive_member": original, "sha256": sha(blobs[original]),
                        "document_kind": "assessment" if "assessment" in docs[original] else "rule",
                        **selected[original]})
    record = {
        "format": "scap-ng-editor-real-smoke/0.1",
        "classification": "source_backed_pre_alpha_authoring_not_runtime_evidence",
        "source_repository": "vanderpol/scap-ng",
        "source_tag": SOURCE_TAG,
        "asset": source_zip.name,
        "asset_sha256": sha(data),
        "review_manifest_sha256": sha(review_manifest.read_bytes()),
        "warning": "r3 scope vocabulary is a research candidate; contextual files may retain 0.3.0. Native 0.4 compilation, scanner semantics, optional foreach and procedural conditional rewrites are NOT proven.",
        "cases": cases,
        "files": entries,
        "counts": {"cases": len(cases), "files": len(entries),
                   "source_rules": sum(x["document_kind"] == "rule" for x in entries),
                   "unique_assessments": sum(x["document_kind"] == "assessment" for x in entries)}
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    return record


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-zip", type=Path, required=True)
    p.add_argument("--review-manifest", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("focused-fixtures/source-backed"))
    p.add_argument("--report", type=Path, default=Path("manifests/pinned-real-stig-fixtures.json"))
    a = p.parse_args()
    print(json.dumps(generate(a.source_zip, a.review_manifest, a.output, a.report)["counts"]))


if __name__ == "__main__":
    main()
