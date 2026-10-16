"""Offline, source-backed fixture seeder contract tests. Refs #1."""
import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import seed_pinned_stig_fixtures as seed


class SeederTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root / "scap-ng-v0.4-joval-six-stig-yaml.zip"
        self.review = self.root / "REVIEW-MANIFEST.json"
        self.output = self.root / "focused-fixtures/source-backed"
        self.report = self.root / "manifests/pinned-real-stig-fixtures.json"
        self.entries = {}
        for benchmark, sv, _ in seed.CASES:
            self.entries[f"authoring/{benchmark}/rules/{sv}.rule.yaml"] = (
                f"rule:\n  id: {sv}\n  default_assessment_choice: automated\n"
                f"  assessment_choices:\n    automated:\n      assessment: {sv}.auto\n")
            self.entries[f"authoring/{benchmark}/assessments/{sv}.automated.yaml"] = (
                f"assessment:\n  id: {sv}.auto\n  mode: automated\n"
                f"  specification:\n    version: 0.4.0\n  tests: {{}}\n")

    def build(self):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as zipf:
            for name, content in self.entries.items():
                zipf.writestr(name, content)
        data = stream.getvalue()
        self.archive.write_bytes(data)
        self.review.write_text(json.dumps(
            {"archives": [{"file": self.archive.name,
                            "sha256": hashlib.sha256(data).hexdigest()}]}))

    def run_seed(self):
        return seed.generate(self.archive, self.review, self.output, self.report)

    def test_exact_bytes_and_manifest(self):
        self.build()
        record = self.run_seed()
        self.assertEqual(record["counts"], {"cases": 6, "files": 12,
                         "source_rules": 6, "unique_assessments": 6})
        for path, content in self.entries.items():
            self.assertEqual((self.output / path).read_bytes(), content.encode())

    def test_real_source_folder_names_are_not_fixed(self):
        original = self.entries.pop("authoring/windows_11/rules/SV-253254.rule.yaml")
        self.entries["authoring/ms_windows_11_v2r10/rules/SV-253254.rule.yaml"] = original
        original_assessment = self.entries.pop(
            "authoring/windows_11/assessments/SV-253254.automated.yaml")
        self.entries["authoring/ms_windows_11_v2r10/assessments/SV-253254.automated.yaml"] = original_assessment
        self.build()
        record = self.run_seed()
        self.assertEqual(record["counts"]["cases"], 6)
        self.assertTrue((self.output / "authoring/ms_windows_11_v2r10/rules/SV-253254.rule.yaml").exists())

    def test_wrong_digest_fails(self):
        self.build()
        self.review.write_text(json.dumps(
            {"archives": [{"file": self.archive.name, "sha256": "0" * 64}]}))
        with self.assertRaisesRegex(ValueError, "checksum"):
            self.run_seed()

    def test_missing_rule_fails(self):
        del self.entries["authoring/rhel_9/rules/SV-257851.rule.yaml"]
        self.build()
        with self.assertRaisesRegex(ValueError, "Rule absent"):
            self.run_seed()

    def test_missing_assessment_fails(self):
        del self.entries["authoring/rhel_9/assessments/SV-257851.automated.yaml"]
        self.build()
        with self.assertRaisesRegex(ValueError, "Unresolved automated"):
            self.run_seed()

    def test_duplicate_assessment_id_fails(self):
        self.entries["authoring/shared/assessments/duplicate.yaml"] = \
            self.entries["authoring/rhel_9/assessments/SV-257851.automated.yaml"]
        self.build()
        with self.assertRaisesRegex(ValueError, "Ambiguous Assessment ID"):
            self.run_seed()

    def test_missing_transitive_dependency_fails(self):
        p = "authoring/rhel_9/assessments/SV-257851.automated.yaml"
        self.entries[p] += "  dependencies:\n    other:\n      assessment: missing.remote\n"
        self.build()
        with self.assertRaisesRegex(ValueError, "Missing Assessment dependency"):
            self.run_seed()


if __name__ == "__main__":
    unittest.main()
