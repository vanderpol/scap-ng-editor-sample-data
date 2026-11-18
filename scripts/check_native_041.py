#!/usr/bin/env python3
"""Validate new 0.4.1 native Assessment fixtures and deliberately invalid examples.

Requires PyYAML and, for full schema validation, jsonschema and referencing.
Does not execute RI and never interprets the separate expected-outcome manifest.
"""
import argparse
from hashlib import sha1
import json
from pathlib import Path
import subprocess

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "fixtures" / "native-041"


def blob_sha(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def audit(canonical: Path | None) -> None:
    manifest = json.loads((BASE / "manifest.json").read_text())
    assert manifest["format"] == "scap-ng/editor-native-language-conformance/1"
    positive, negative = manifest["positive"], manifest["negative"]
    assert len(positive) >= 6 and len(negative) >= 3
    registry = validator = None
    if canonical:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import ValidationError
        from referencing import Registry, Resource

        head = subprocess.check_output(
            ["git", "-C", str(canonical), "rev-parse", "HEAD"], text=True
        ).strip()
        assert head == manifest["schema_source"]["commit"], (head, manifest["schema_source"]["commit"])
        registry = Registry()
        for path in (canonical / "schema").glob("*.schema.json"):
            schema = json.loads(path.read_text())
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        schema = json.loads((canonical / "schema/assessment.schema.json").read_text())
        validator = Draft202012Validator(schema, registry=registry)

    seen = set()
    for status, fixtures in [("valid", positive), ("invalid", negative)]:
        for fixture in fixtures:
            relative = fixture["path"]
            assert relative not in seen and relative.startswith("fixtures/native-041/")
            assert ".." not in Path(relative).parts
            seen.add(relative)
            raw = (ROOT / relative).read_bytes()
            assert blob_sha(raw) == fixture["git_blob_sha"], relative
            doc = yaml.safe_load(raw)
            assert isinstance(doc, dict) and isinstance(doc.get("assessment"), dict), relative
            assert doc["assessment"].get("specification", {}).get("version") == "0.4.1"
            assert "expected" not in doc and "golden" not in doc
            if validator:
                if status == "valid":
                    validator.validate(doc)
                else:
                    try:
                        validator.validate(doc)
                    except ValidationError:
                        pass
                    else:
                        raise AssertionError("negative fixture unexpectedly schema-valid: " + relative)
            else:
                print("UNVERIFIED SCHEMA (pass --canonical-root):", relative)

    policy_docs = manifest.get("policy_documents", [])
    semantic_negatives = manifest.get("semantic_negative", [])
    for fixture in policy_docs + semantic_negatives:
        relative = fixture["path"]
        assert relative not in seen and relative.startswith("fixtures/native-041/")
        assert ".." not in Path(relative).parts
        seen.add(relative)
        raw = (ROOT / relative).read_bytes()
        assert blob_sha(raw) == fixture["git_blob_sha"], relative
        doc = yaml.safe_load(raw)
        assert isinstance(doc, dict), relative
        if canonical:
            schema_file = fixture.get("schema", "assessment.schema.json")
            schema = json.loads((canonical / "schema" / schema_file).read_text())
            Draft202012Validator(schema, registry=registry).validate(doc)

    for fixture in manifest.get("policy_vectors", []):
        relative = fixture["path"]
        assert relative not in seen and relative.startswith("fixtures/native-041/")
        assert ".." not in Path(relative).parts
        seen.add(relative)
        raw = (ROOT / relative).read_bytes()
        assert blob_sha(raw) == fixture["git_blob_sha"], relative
        obj = json.loads(raw)
        assert obj.get("kind") == "synthetic-applicability-tree-not-a-benchmark", relative

    print(f"PARSED {len(positive)} Assessments / {len(policy_docs)} policy documents / {len(negative)} syntax-invalid / {len(semantic_negatives)} semantic-negative / {len(manifest.get('policy_vectors', []))} logic vectors; schema_checked={bool(validator)}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path)
    options = parser.parse_args()
    audit(options.canonical_root)
