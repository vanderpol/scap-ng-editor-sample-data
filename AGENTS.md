# Guidance for agents working on SCAP-NG VS Code sample data

- Keep this repository **small, editor-focused and provenance-pinned**. Authoritative schemas and examples are in `vanderpol/scap-ng`, converter and normalizers in `vanderpol/scap-ng-tools`, proof/corpus artifacts in `vanderpol/scap-ng-evidence`. The private research repository is not an editor build dependency.
- The working schema pin is `354c9c962c77488a3d939cab56f6ceecfd495d27` on canonical [PR #4](https://github.com/vanderpol/scap-ng/pull/4), physically flat under `schema/`. Never use private research paths or assume moving `main` is the frozen version.
- Test `require` uses `item_requirement: {items_found: ..., items_satisfying: ...}` before sibling `field_requirement`. An existence-only Test uses `item_requirement: {items_found: ...}`; do not invent `items_satisfying`. Result wire fields remain unchanged.
- Preserve original fixture bytes. For edit tests, work on copies or reversible buffers; verify no-op save and exact undo. Malformed YAML is intentional.
- Never promote a draft/warning or a compiling Assessment to source-proved or scanner-runtime-equivalent status.
- Do not copy in the 65-STIG corpus or restart retired r3 seeding workflows. Use pinned external review assets for scale tests.
- All editor defaults are presentation metadata only. Actual values in saved YAML remain explicit; no runtime/validation default is inferred.
- Update `fixtures/manifest.json` with every deliberate fixture addition or source-pin change. New fixtures require a concrete editor test purpose and honest proof status.
- Prior data is recoverable at archive/pre-vscode-cleanup-20261101. Never rewrite or delete that branch as part of routine editor work.
