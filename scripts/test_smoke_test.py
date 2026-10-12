import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from smoke_test import validate_health, verify


class DeployVerificationTests(unittest.TestCase):
    def test_old_version_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_health({"status": "ok", "ambiente": "Staging", "versao": "old"}, "Staging", "new")

    def test_wrong_environment_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_health({"status": "ok", "ambiente": "Production", "versao": "new"}, "Staging", "new")

    def test_unhealthy_database_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_health({"status": "unhealthy"}, "Staging", "new")

    def test_retry_waits_for_new_revision_and_queries_database(self):
        old = {"status": "ok", "ambiente": "Staging", "versao": "old"}
        new = {**old, "versao": "new"}
        with tempfile.TemporaryDirectory() as directory:
            with patch("smoke_test.get_json", side_effect=[old, new, []]) as request:
                evidence = verify("http://localhost", "Staging", "new", str(Path(directory) / "result.json"), 2, 0)
                self.assertTrue(evidence["success"])
                self.assertEqual(evidence["attempt"], 2)
                self.assertTrue(request.call_args.args[0].endswith("/api/cidades/ranking"))

    def test_invalid_ranking_fails_and_saves_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            with patch("smoke_test.get_json", side_effect=[
                {"status": "ok", "ambiente": "Staging", "versao": "new"}, {"error": "database"}
            ]):
                with self.assertRaises(RuntimeError):
                    verify("http://localhost", "Staging", "new", str(output), 1, 0)
            self.assertIn('"success": false', output.read_text())


if __name__ == "__main__":
    unittest.main()
