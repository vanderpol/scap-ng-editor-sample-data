# Native SCAP-NG 0.4.1 language fixtures — independent authoring

This suite tests **SCAP-NG-native authoring and shared evaluation behavior**, especially features missing from the original OVAL Self-Assertion corpus. It is **not** a source STIG benchmark, scanner outcome oracle, or proof of host-wide compliance.

**Schema baseline:** `vanderpol/scap-ng@5ee55288b369da26f308f40813e545b78dff2753` (single 0.4.1 mainline contract).
**Expected outcomes are recorded separately** in [manifest.json](manifest.json); no golden outcome is injected into an Assessment, and no source content is modified to force an expected answer.

| Fixture | Language or editing behavior | Source comparison |
|---|---|---|
| `conditional-ordered.assessment.yaml` | First TRUE branch wins; skipped branches, `if/then/else_if/else` | Native-only |
| `conditional-not-applicable.assessment.yaml` | Explicit `not_applicable` vs `not_evaluated` | Native-only authoring |
| `optional-input-presence.assessment.yaml` | Optional organizational Input presence (missing vs provided empty vs value) | Canonical 0.4.1 example copied unchanged |
| `require-one-versus-xor.assessment.yaml` | ONE ≠ XOR under three TRUE per-Item branches; independent field cardinality | Native logical syntax; source concept overlaps OVAL |
| `set-filter-difference.assessment.yaml` | Difference with include/exclude filters on typed Items | OVAL has analogous constructs; native shape is different |
| `shared-object-reuse.assessment.yaml` | Same shared Object referenced from two Tests | Native authoring/reuse behavior |
| `referenced-baseline.assessment.yaml` / `conditional-dependency.assessment.yaml` | Cross-Assessment dependencies, first-class conditional dependency truth, reuse | Native authoring |
| `manual-review.assessment.yaml` | Manual procedures, human response choices, normalized technical outcomes | Native manual authoring |
| `policy/benchmark-applicability-profiles.benchmark.yaml` plus two Rules and an applicability catalog | Benchmark + nested Group + Rule-local applicability, two independent disabled-only Profiles, Assessment choice | Native policy authoring beyond OVAL Self-Assertion |
| `applicability/inheritance-vector.json` | Benchmark + nested Group + Rule ancestor logic, status propagation | Synthetic logic vector, **not** a canonical Benchmark document |

`semantic-negative/` contains **semantically rejected** authoring examples (unguarded optional Input and dangling shared Object references) that may still pass JSON Schema syntax. Both editor semantic analysis and RI package admission should diagnose these without inventing facts.

`negative/` contains **deliberately schema-invalid** cases for the wrong `elseif` spelling, obsolete Variable declaration `datatype`, and the unapproved Evaluate `foreach` syntax. These must never be opened as valid example content or admitted by the scanner.

## How to validate

With Python 3, PyYAML and jsonschema/referencing installed, clone/pin the canonical repo to the exact commit above:

```bash
python scripts/check_native_041.py --canonical-root /path/to/scap-ng-at-5ee55288
```

The check verifies Git blob identities, syntax, current canonical 0.4.1 schema admission for valid Assessments and schema **rejection** for negatives. It does **not** execute the RI, prove expected outcomes, or silently change the upstream schemas. An RI conformance harness must run the shared evaluator using synthetic, typed evidence and record actual outcomes independently in the evidence repository.

## Authoring and execution rules

- Treat absolute `/tmp/scap-ng-fixture-*` selectors as **placeholders**. Never assume host files exist or make their absence a compliance PASS.
- `variable.value` tests are virtual, with no real host collector. This is intentional so that Linux and later Windows can execute the **same core engine**.
- For Set/Filter and shared-Object fixtures, supply controlled Items with provenance, distinct IDs, proper field typing, complete/incomplete collection receipts and limits. Native host scans are a separate qualification.
- Include editor round-trip checks: Evaluate-first ordering, Variables bottom, key/branch renames, nested logical changes, comments, no-op byte stability and Undo/Redo.
- No `foreach` runtime implementation is authorized by this fixture. Canonical [issue #76](https://github.com/vanderpol/scap-ng/issues/76) is the design/owner-approval gate.
- Keep original 0.4.0 examples under `fixtures/current-v04/` as **historical migration inputs only** until the editor team verifies no consumer needs them.

## Status

**Schema admission PASSED** on 2026-11-18 for all 9 Assessments and 4 policy documents; the three intentional schema-invalid files were rejected and the two semantic-negative examples remained structurally valid. [Native 0.4.1 CI run](https://github.com/vanderpol/scap-ng-editor-sample-data/actions/runs/44358520526) executed and passed at PR #5 head `401d94290b54cacfa81300d483d0959033470ff9`; historical 0.4 fixture CI also passed. **RI execution, independent expected-result comparison, semantic-negative diagnostics and VS Code graphical/YAML roundtrips remain pending.** Do not report scanner PASS counts for these fixtures before those steps execute.
