# Sample repository retention audit — 2026-11-18

The mainline repository was previously reduced from a 2,000+-file r3 catalog to a **small curated workspace**. Recovery archive: `archive/pre-vscode-cleanup-20261101`. Do not purge/rewrite that branch.

| Existing path | Status | Action |
|---|---|---|
| `fixtures/current-v04/` | Four exact canonical 0.4.0 Assessments + derived Linux JSON; manifest pinned to `463675f`; obsolete **as current 0.4.1 grammar examples** | Keep temporarily as **legacy migration/regression** fixtures. Do not feed them to the 0.4.1 RI acceptance lane. Ticket editor team to assess use, then migrate/repoint to canonical 0.4.1 and archive/delete only with consumer proof |
| `fixtures/source-preservation/` | Annotated YAML/JSON and intentionally incomplete draft; useful for lossless editing and diagnostics, not scanner content | **Retain** as editor-only fixtures; no canonical schema validity claim for malformed documents |
| `fixtures/manifest.json` | Honest provenance for old exact 0.4.0 bytes, but not the current schema pin | Retain for legacy reproducibility, mark as historical |
| `scripts/check_fixtures.py` | Verifies **only** old `current-v04` and old canonical ref | Retain as migration regression check, run separately from new 0.4.1 script |
| Historical auto-seeding and prior 2,000+ r3 files | Already on archival branch | Do **not** restore on active main; reference external evidence/source libraries |
| `fixtures/native-041/` | New small current-schema native semantic examples and negative guards | Promote after exact pinned validator and RI/editor acceptance evidence |

Quick code search of `vanderpol/scap-ng-vscode`, RI and Tools did **not** find a direct text reference to this repository name or to `current-v04`. Search absence does **not** prove that CI, installed extensions or developer workflows never use these files. Do not remove old fixtures without a consumer inventory.

**Recommendation:** keep this repository as the **small, pinned native language + editor regression source**, but separate the semantic conformance corpus from editor-only lossy-preservation tests. Large converted STIG benchmarks and scan outputs belong in `scap-ng-evidence`, never here.
