# SCAP-NG VS Code editor sample data

This is a **small, intentionally curated starter workspace** for [scap-ng-vscode](https://github.com/vanderpol/scap-ng-vscode). It is not the authoritative SCAP-NG corpus, schema, specification, a complete STIG, or scanner evidence.

## Start here

- **Authoring contract:** SCAP-NG 0.4.0 pre-alpha, draft [PR #268](https://github.com/vanderpol/scap-ng/pull/268), pinned at `37b614858c9f6f1d6261fac244cb734c8acc060b`.
- **Editor adapter checkpoint:** [`ae7f81259`](https://github.com/vanderpol/scap-ng-vscode/commit/ae7f812590fa108b412146f21e59171d60507f29). The editor still needs an extension host, graphical UI, native VS Code edits, and a regex/sample playground.
- **Samples:** [`fixtures/current-v04/`](fixtures/current-v04/) has three real-source-backed automated Assessments (Linux, Windows registry, Windows permissions). These validate/compile statically at the cited source checkpoint but do **not** establish scanner-runtime equivalence.
- **Editing edge cases:** [`fixtures/source-preservation/`](fixtures/source-preservation/) has valid annotated YAML, valid JSON, and deliberately malformed YAML for lossless round-trip and diagnostics. These are *not* normative SCAP-NG documents.
- **Inventory:** [`fixtures/manifest.json`](fixtures/manifest.json) gives exact upstream provenance and expected editor uses.

## Suggested first editor smoke tests

1. Open each source file without changing a byte; verify a no-op save is byte-identical.
2. Edit a scalar in YAML and verify comments, quotes, order, and unrelated formatting survive; undo exactly.
3. Show schema-driven help/enums/defaults from an **externally selected, SHA-verified 0.4 metadata pack**; hidden defaults must remain explicitly serialized and diagnostics visible.
4. Open malformed YAML without destroying it. Surface a precise error and allow text editing.
5. Exercise Linux/Windows Assessment navigation and explicit source selection. Do not assert PASS/FAIL without a qualified evaluator.

## Large-scale STIG library tests

Do **not** expand the old r3 catalog in this repository. When navigation/performance tests need scale, obtain a pinned, immutable full-65 review download through the [SCAP-NG downloads index](https://github.com/vanderpol/scap-ng/blob/main/docs/releases/0.4.0-downloads-and-samples.md) and verify its published manifest and hashes first. That DRAFT includes unverified, blocked and manual content: do not label it a deployable or fully scanner-proved STIG library.

## Archived material

The entire former `main` tree, including the 2,000+ file r3 RHEL9/Windows11 catalog, older preview fixtures, seeding workflows and source-cache research, is preserved unchanged in [`archive/pre-vscode-cleanup-20261101`](https://github.com/vanderpol/scap-ng-editor-sample-data/tree/archive/pre-vscode-cleanup-20261101), starting at `cb5a264f6684433616ede83cdfb30472d92470e2`. This branch is a recovery archive, not an active generation target.

The current `main` intentionally has no auto-seeding workflow: sample refreshes must be deliberate, pinned to a new source/schema/editor revision, validated and recorded in the fixture manifest. No schemas, compiled bundles, source archives, or proof packages are vendored here.

Publisher-origin data and existing provenance remain subject to their respective upstream terms; this repository does not assert a new project-wide source/specification license.
