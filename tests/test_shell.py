"""Tests for pysh shell."""
import unittest
from pysh.shell import PyShell


class TestPyShell(unittest.TestCase):
    def setUp(self):
        self.shell = PyShell()

    def test_aliases(self):
        self.assertIn("ll", self.shell.aliases)
        self.assertEqual(self.shell.aliases["ll"], "ls -la")

    def test_history(self):
        self.shell.history.append("test command")
        self.assertIn("test command", self.shell.history)

    def test_highlight_no_error(self):
        result = self.shell._highlight("git status")
        self.assertIsInstance(result, str)

    def test_suggest(self):
        self.shell.history = ["git status", "git push", "cd src"]
        suggestions = self.shell._suggest("git")
        self.assertGreaterEqual(len(suggestions), 1)
        for s in suggestions:
            self.assertTrue(s.startswith("git"))


if __name__ == "__main__":
    unittest.main()
