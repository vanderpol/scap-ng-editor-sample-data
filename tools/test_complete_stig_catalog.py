"""Self-contained tests for exact-source complete STIG extraction (Refs #1 #2)."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from seed_complete_stig_catalog import generate, digest


def rule(id, target):
    return ("rule:\n  id: " + id + "\n  title: Rule " + id +
            "\n  assessment_choices:\n    automated:\n      assessment: " + target + "\n").encode()


def assessment(id, reference=None):
    expression = "  evaluate:\n    assessment: " + reference if reference else (
        "  evaluate:\n    test: t\n  tests:\n    t:\n      test_title: Simple match\n      capability: unix.file\n      states:\n      - name:\n          equals: test\n")
    return ("assessment:\n  id: " + id + "\n  mode: automated\n" + expression + "\n").encode()


class CompleteSTIGCatalogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.asset = self.root / "source.zip"
        self.review = self.root / "REVIEW-MANIFEST.json"
        self.files = {
            "authoring/rhel_9/rules/SV-100.rule.yaml": rule("SV-100", "shared-check"),
            "authoring/rhel_9/rules/SV-101.rule.yaml": rule("SV-101", "rhel-check"),
            "authoring/ms_windows_11/rules/SV-200.rule.yaml": rule("SV-200", "win-check"),
            "authoring/shared/assessments/shared.yaml": assessment("shared-check"),
            "authoring/rhel_9/assessments/automated/rhel.yaml": assessment("rhel-check", "shared-check"),
            "authoring/ms_windows_11/assessments/automated/win.yaml": assessment("win-check"),
        }

    def build(self):
        with zipfile.ZipFile(self.asset, "w") as archive:
            for name, data in self.files.items():
                archive.writestr(name, data)
        self.review.write_text(json.dumps({
            "archives": [{"file": self.asset.name, "sha256": digest(self.asset.read_bytes())}]
        }))

    def test_complete_rules_and_shared_assessment_closure(self):
        self.build()
        output = self.root / "complete-stigs"
        manifest = generate(self.asset, self.review, output)
        self.assertEqual(manifest["stig_count"], 2)
        self.assertEqual(manifest["rule_count"], 3)
        self.assertEqual(manifest["assessment_count"], 3)
        self.assertEqual(manifest["unresolved_assessment_refs"], [])
        self.assertEqual(
            (output / "authoring/shared/assessments/shared.yaml").read_bytes(),
            self.files["authoring/shared/assessments/shared.yaml"],
        )
        index = json.loads((output / "rhel_9/index.json").read_text())
        self.assertEqual(index["rule_count"], 2)
        self.assertTrue(all(r["assessment_choices"]["automated"]["loaded"] for r in index["rules"]))
        self.assertTrue(all(r["rule_path"].startswith("complete-stigs/") for r in index["rules"]))

    def test_bad_archive_digest_fails_closed(self):
        self.build()
        self.review.write_text('{"archives":[{"file":"source.zip","sha256":"bad"}]}')
        with self.assertRaisesRegex(ValueError, "Unverified"):
            generate(self.asset, self.review, self.root / "complete-stigs")

    def test_missing_assessment_fails(self):
        self.files.pop("authoring/shared/assessments/shared.yaml")
        self.build()
        with self.assertRaisesRegex(ValueError, "Incomplete assessment closure"):
            generate(self.asset, self.review, self.root / "complete-stigs")

    def test_unknown_stig_source_fails(self):
        self.files.pop("authoring/rhel_9/rules/SV-100.rule.yaml")
        self.files.pop("authoring/rhel_9/rules/SV-101.rule.yaml")
        self.build()
        with self.assertRaisesRegex(ValueError, "has no Rule"):
            generate(self.asset, self.review, self.root / "complete-stigs")


if __name__ == "__main__":
    unittest.main()
