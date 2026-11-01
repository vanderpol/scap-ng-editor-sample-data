# Guidance for agents working on SCAP-NG VS Code sample data

- Keep this repository **small, editor-focused and provenance-pinned**. The authoritative SCAP-NG schema, converter, compiler and proofs remain in vanderpol/scap-ng and scap-ng-evidence.
- The current working schema pin is 37b614858c9f6f1d6261fac244cb734c8acc060b on draft PR #268; do not silently substitute `main` or claim it is a frozen 0.4 release.
- Preserve original fixture bytes. For edit tests, work on copies or reversible buffers; verify no-op save and exact undo. Malformed YAML is intentional.
- Never promote a draft/warning or a compiling Assessment to source-proved or scanner-runtime-equivalent status.
- Do not copy in the 65-STIG corpus or restart retired r3 seeding workflows. Use pinned external review assets for scale tests.
- All editor defaults are presentation metadata only. Actual values in saved YAML remain explicit; no runtime/validation default is inferred.
- Update `fixtures/manifest.json` with every deliberate fixture addition or source-pin change. New fixtures require a concrete editor test purpose and honest proof status.
- Prior data is recoverable at archive/pre-vscode-cleanup-20261101. Never rewrite or delete that branch as part of routine editor work.
