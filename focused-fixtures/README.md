# Focused Editor Fixtures

Small positive, negative, boundary and source-preservation fixtures. See [the machine-readable fixture inventory](../manifests/editor-smoke-fixtures.json) and [issue #1](https://github.com/vanderpol/scap-ng-editor-sample-data/issues/1).

## Available now — synthetic editor plumbing, not valid STIG checks

- `source-preservation/annotated-draft.yaml`: YAML parses; preserve original comments, quotes, key order and unknown fields; no schema validity asserted.
- `source-preservation/incomplete-draft.yaml`: intentionally malformed YAML; keep editable, report exact parser location and do not destroy it on save.
- `source-preservation/annotated-draft.json`: JSON parses; byte-identical no-op save and surgical editing; no SCAP-NG schema validity asserted.

## Real, source-backed Assessments — generated and verified

The [pinned r3 real-STIG manifest](../manifests/pinned-real-stig-fixtures.json) now lists **12 verified authoring documents** (six real Rules, six automated Assessments) extracted without rewriting them from the r3 preview archive; [GitHub Actions run 38833981101](https://github.com/vanderpol/scap-ng-editor-sample-data/actions/runs/38833981101) passed **7** fail-closed offline tests, source archive SHA-256 checking, logical Rule/Assessment resolution, local Variable/Object checks, and source-byte verification. The examples include RHEL9 SV-257851/SV-257889, Win11 SV-253254/SV-253495, Apache SV-214228 and DNS SV-259345. The release directory names are deliberately preserved as downloaded, including `ms_windows_11` and `apache_server_2-4_unix_server`.

The `source-backed/` tree is regenerated only from the checksum-pinned archive using [the seeding tool](../tools/seed_pinned_stig_fixtures.py). It is authoring source, **not** a normative 0.4 grammar or runnable 0.4 package. Do not manually recast the `for_each`/conditional research illustrations as source-equivalent changes.

## Further corpus expansion (not a first-slice blocker)

Expand the corpus only where a new editor test needs additional real cases or multi-file dependency complexity. The source of truth remains [the Joval six-STIG r3 authoring prerelease](https://github.com/vanderpol/scap-ng/releases/tag/v0.4.0-joval-meeting-preview-20261015-r3); 0.4 compiler and live semantic conformance remain separately gated.

The real files are ready for editor #3's source-roundtrip acceptance testing, **but no editor implementation or editor round-trip test is claimed yet**. Do not copy schemas or compiled bundles here.
