# Focused Editor Fixtures

Small positive, negative, boundary and source-preservation fixtures. See [the machine-readable fixture inventory](../manifests/editor-smoke-fixtures.json) and [issue #1](https://github.com/vanderpol/scap-ng-editor-sample-data/issues/1).

## Available now — synthetic editor plumbing, not valid STIG checks

- `source-preservation/annotated-draft.yaml`: YAML parses; preserve original comments, quotes, key order and unknown fields; no schema validity asserted.
- `source-preservation/incomplete-draft.yaml`: intentionally malformed YAML; keep editable, report exact parser location and do not destroy it on save.
- `source-preservation/annotated-draft.json`: JSON parses; byte-identical no-op save and surgical editing; no SCAP-NG schema validity asserted.

## Still required before real-source acceptance

Populate the actual **immutable r3** Linux/Windows source-backed Assessment examples plus their complete required referenced dependencies. The source of truth is [the Joval six-STIG r3 authoring prerelease](https://github.com/vanderpol/scap-ng/releases/tag/v0.4.0-joval-meeting-preview-20261015-r3). Record exact archive member path and digest, pinned release identity, native version, and independent schema/reference status in the manifest; do not fabricate or silently simplify `for_each`, `if/else`, Windows record, or Variable semantics.

These synthetic fixtures can unblock parser API design but **cannot** satisfy the real-STIG MVP proof in [editor #3](https://github.com/vanderpol/scap-ng-editor/issues/3). Do not copy schemas or compiled bundles here.
