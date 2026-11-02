#!/usr/bin/env python3
"""Verify the small 0.4 editor fixtures and optionally their exact schema pin.

No network or corpus downloads. Use --canonical-root with a checkout at the
manifest's recorded commit for full Draft 2020-12 validation.
"""

import argparse
from hashlib import sha1
import json
from pathlib import Path
import subprocess

import yaml


ROOT = Path(__file__).resolve().parents[1]


def git_blob(raw):
    return sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def check(canonical=None):
    manifest = json.loads((ROOT / 'fixtures/manifest.json').read_text())
    assert manifest['format'] == 'scap-ng/editor-starter-fixtures/1'
    paths = set()
    for fixture in manifest['fixtures']:
        path = fixture['path']
        assert path not in paths and not Path(path).is_absolute() and '..' not in Path(path).parts
        paths.add(path)
        raw = (ROOT / path).read_bytes()
        if 'git_blob_sha' in fixture:
            assert git_blob(raw) == fixture['git_blob_sha'], path
        if path.startswith('fixtures/current-v04/'):
            document = (yaml.safe_load(raw) if path.endswith('.yaml') else json.loads(raw))
            for test in document['assessment']['tests'].values():
                req = test['require']
                assert 'items_found' not in req and 'items_satisfying' not in req
                assert list(req['item_requirement']) == ['items_found', 'items_satisfying']
    present = {p.relative_to(ROOT).as_posix()
               for p in (ROOT / 'fixtures/current-v04').iterdir() if p.is_file()}
    assert present == {p for p in paths if p.startswith('fixtures/current-v04/')}
    linux = ROOT / 'fixtures/current-v04/linux-home-nosuid.assessment'
    assert yaml.safe_load(Path(str(linux) + '.yaml').read_text()) == json.loads(
        Path(str(linux) + '.json').read_text())

    if canonical is not None:
        import jsonschema
        from referencing import Registry, Resource
        assert subprocess.check_output(['git', '-C', str(canonical), 'rev-parse', 'HEAD'],
                                       text=True).strip() == manifest['schema_source']['ref']
        registry = Registry()
        for path in (canonical / 'schema').glob('*.schema.json'):
            schema = json.loads(path.read_text())
            registry = registry.with_resource(schema['$id'], Resource.from_contents(schema))
        main = json.loads((canonical / 'schema/assessment.schema.json').read_text())
        validator = jsonschema.Draft202012Validator(main, registry=registry)
        for fixture in manifest['fixtures']:
            upstream = fixture.get('upstream', '')
            if not upstream.startswith('examples/'):
                continue
            raw = (ROOT / fixture['path']).read_bytes()
            assert raw == (canonical / upstream).read_bytes(), fixture['path']
            validator.validate(yaml.safe_load(raw))
    return len(paths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canonical-root', type=Path)
    args = parser.parse_args()
    count = check(args.canonical_root)
    print(f'VERIFIED: {count} small editor fixtures, no legacy item keys')
