# SCAP-NG Editor Sample Data

External sample and scale-test content for `vanderpol/scap-ng-editor`.

This repository exists so the editor can remain small, transferable, and independent of ownership of the SCAP-NG standards/content project.

## Purpose

The editor is expected to consume and edit the full complexity of real SCAP-NG content. This repository therefore contains substantial generated data, not only tiny unit-test fixtures.

The primary corpus should be derived reproducibly from the pinned 65-benchmark NIWC Current corpus using the authoritative SCAP-NG conversion and exact-normalization pipeline.

## Three generated views

The repository is organized around the editor's three first-class use cases:

```text
stig-manual/
scap-ng/
assessments-only/
manifests/
focused-fixtures/
```

### `stig-manual/`

A prose-oriented export for benchmark/manual authoring.

It should preserve the Benchmark, groups, Rules, references, profiles and other policy/prose structures needed to author a STIG manual while excluding automated Assessment payloads from the working view.

This is a generated view, not a separately maintained source corpus.

### `scap-ng/`

The complete normalized SCAP-NG authoring source derived from the full corpus.

This is the broadest scale and complexity test for the editor and should preserve the complete source graph, including shared/reusable Assessments and cross-file references.

### `assessments-only/`

An export containing the Assessment authoring surface independently of Benchmark prose.

It should contain enough surrounding identity/reference information to make reusable Assessments understandable and editable without creating synthetic Benchmark wrappers.

This is also a generated view of the same normalized corpus.

## One source, three exports

The three large directories SHALL be reproducibly derived from one pinned normalized source build. They SHALL NOT evolve independently.

Every refresh should record at least:

- SCAP-NG source commit;
- pinned NIWC source revision;
- schema version;
- conversion command/workflow;
- normalization command/workflow;
- export generator version/commit;
- counts of benchmarks, rules, assessments, tests, objects, states and variables where practical;
- known blockers/exclusions.

The `manifests/` directory should carry this provenance and per-export inventory.

## Scale is intentional

These exports should be large enough to exercise:

- startup and project-load behavior;
- directory/tree navigation;
- search across many files;
- cross-file reference resolution;
- shared Assessment discovery;
- validation throughput;
- diagnostics at scale;
- save/round-trip behavior;
- memory usage;
- UI responsiveness for large Benchmarks and Assessment libraries.

Do not reduce the main corpus to toy examples merely to make the editor easier to implement.

## Focused fixtures

`focused-fixtures/` may contain small positive, negative, boundary, and round-trip cases for fast automated tests.

These supplement the large corpus; they do not replace it.

## What does not belong here

- editor application source code;
- normative SCAP-NG schema/specification source;
- independently hand-maintained copies of the same corpus in the three views;
- unrelated generated review/evidence products.

## Generation rule

Generated content may be committed here because exercising large real-world editor workloads is the purpose of this repository. Generation must remain reproducible and provenance-pinned.
