# SCAP-NG Editor Sample Data

External sample and test content for `vanderpol/scap-ng-editor`.

This repository exists so the editor can remain small, transferable, and independent of ownership of the SCAP-NG content project.

## What belongs here

- small representative SCAP-NG documents used by editor tests;
- positive examples that should validate;
- negative examples that intentionally fail validation;
- round-trip fixtures that exercise preservation of unknown or future fields;
- focused samples for new SCAP-NG features as those features stabilize.

## What does not belong here

- the SCAP-NG specification or normative schema source;
- full converted benchmark corpora unless a narrowly scoped editor test truly requires them;
- generated review builds;
- editor source code;
- duplicate copies of large content already maintained elsewhere.

## Suggested layout

```text
fixtures/
  v0.2.0/
    valid/
    invalid/
    round-trip/
  future/
    README.md
manifests/
  fixtures.json
```

The directory structure is intentionally versioned so editor behavior can be tested against more than one SCAP-NG schema snapshot without rewriting or replacing earlier fixtures.

## Fixture rule

Every fixture added here should have a clear test purpose. Prefer the smallest document that demonstrates the behavior under test.
