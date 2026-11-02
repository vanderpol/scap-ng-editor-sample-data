# SCAP-NG VS Code editor sample data

This is a **small, intentionally curated starter workspace** for [scap-ng-vscode](https://github.com/vanderpol/scap-ng-vscode). It is not the authoritative SCAP-NG corpus, schema, specification, a complete STIG, or scanner evidence.

## Start here

- **Authoring contract:** SCAP-NG 0.4.0 pre-release Item grouping amendment, [canonical PR #4](https://github.com/vanderpol/scap-ng/pull/4), pinned at `354c9c962c77488a3d939cab56f6ceecfd495d27`. Flat `schema/` is authoritative; versioned `$id` URIs still contain `v0.4.0`.
- **Editor adapter checkpoint:** [`e3ac527`](https://github.com/vanderpol/scap-ng-vscode/commit/e3ac52753569e861cc1e0df1a458ecdc023ec1ad). A schema-pin/CI refresh is pending. The editor still needs an extension host, graphical UI, native VS Code edits, and a regex/sample playground.
- **Samples:** [`fixtures/current-v04/`](fixtures/current-v04/) contains four exact canonical Assessments (Linux, Windows registry, Windows permissions, optional organizational Input) and one derived Linux JSON view. These validate structurally against the amended schema, **not** scanner runtime or new independent proof equivalence.
- **Editing edge cases:** [`fixtures/source-preservation/`](fixtures/source-preservation/) has valid annotated YAML, valid JSON, and deliberately malformed YAML for lossless round-trip and diagnostics. These are *not* normative SCAP-NG documents.
- **Inventory:** [`fixtures/manifest.json`](fixtures/manifest.json) gives exact upstream provenance and expected editor uses.

## Suggested first editor smoke tests

The small fixture manifest is independently audited in CI. From a local
checkout with Python, PyYAML and jsonschema installed, run
`python scripts/check_fixtures.py --canonical-root /path/to/pinned-scap-ng`.
The selected source checkout must be the exact commit in `fixtures/manifest.json`.

1. Open each source file without changing a byte; verify a no-op save is byte-identical.
2. Edit a scalar in YAML and verify comments, quotes, order, and unrelated formatting survive; undo exactly.
3. Show schema-driven help/enums/defaults from an **externally selected, SHA-verified 0.4 metadata pack**; hidden defaults must remain explicitly serialized and diagnostics visible.
4. Open malformed YAML without destroying it. Surface a precise error and allow text editing.
5. Exercise Linux/Windows Assessment navigation and explicit source selection. Do not assert PASS/FAIL without a qualified evaluator.

## Large-scale STIG library tests

Do **not** expand the old r3 catalog in this repository. The historical 65-stream review library is in [SCAP-NG Evidence](https://github.com/vanderpol/scap-ng-evidence/tree/main/runs/v04-library/2026-10-30-all65-normalized-review-ff69d46b3); it **predates the owner-approved `item_requirement` amendment** and is not a current-schema fixture. Wait for a new immutable, checksum-verified full library before using it for schema-valid current 0.4 editor tests. Full-scale downloads belong outside this small Git repository.

## Archived material

The entire former `main` tree, including the 2,000+ file r3 RHEL9/Windows11 catalog, older preview fixtures, seeding workflows and source-cache research, is preserved unchanged in [`archive/pre-vscode-cleanup-20261101`](https://github.com/vanderpol/scap-ng-editor-sample-data/tree/archive/pre-vscode-cleanup-20261101), starting at `cb5a264f6684433616ede83cdfb30472d92470e2`. This branch is a recovery archive, not an active generation target.

The current `main` intentionally has no auto-seeding workflow: sample refreshes must be deliberate, pinned to a new source/schema/editor revision, validated and recorded in the fixture manifest. No schemas, compiled bundles, source archives, or proof packages are vendored here.

Publisher-origin data and existing provenance remain subject to their respective upstream terms; this repository does not assert a new project-wide source/specification license.
