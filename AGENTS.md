# Guidance for agents working on SCAP-NG VS Code sample data

- Keep this repository **small, editor-focused and provenance-pinned**. Authoritative schemas and examples are in `vanderpol/scap-ng`, converter and normalizers in `vanderpol/scap-ng-tools`, proof/corpus artifacts in `vanderpol/scap-ng-evidence`. The private research repository is not an editor build dependency.
- **Current native suite:** `fixtures/native-041/` is pinned to canonical `vanderpol/scap-ng@5ee55288b369da26f308f40813e545b78dff2753` (0.4.1). Run `scripts/check_native_041.py --canonical-root <exact pinned checkout>` before claiming schema validity. Expected results live in its separate manifest, not authored Assessments; RI execution and VS Code roundtrip proof are separate qualification gates.
- **Legacy only:** `fixtures/current-v04/` and `fixtures/manifest.json` retain the historical `354c9c...` / `463675...` 0.4.0 pre-release pin for preservation/regression. Do not reuse these as 0.4.1 examples; preserve upstream authoring bytes and archived branch.
- Test `require` uses `item_requirement: {items_found: ..., items_satisfying: ...}` before sibling `field_requirement`. An existence-only Test uses `item_requirement: {items_found: ...}`; do not invent `items_satisfying`. Result wire fields remain unchanged.
- Preserve original fixture bytes. For edit tests, work on copies or reversible buffers; verify no-op save and exact undo. Malformed YAML is intentional.
- Never promote a draft/warning or a compiling Assessment to source-proved or scanner-runtime-equivalent status.
- Do not copy in the 65-STIG corpus or restart retired r3 seeding workflows. Use pinned external review assets for scale tests.
- All editor defaults are presentation metadata only. Actual values in saved YAML remain explicit; no runtime/validation default is inferred.
- Update `fixtures/manifest.json` with every deliberate fixture addition or source-pin change. New fixtures require a concrete editor test purpose and honest proof status.
- Prior data is recoverable at archive/pre-vscode-cleanup-20261101. Never rewrite or delete that branch as part of routine editor work.
