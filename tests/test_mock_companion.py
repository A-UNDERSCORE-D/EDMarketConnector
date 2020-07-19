import unittest

import mock_companion


class TestCompanion(unittest.TestCase):
    def setUp(self) -> None:
        self.mocked = mock_companion.MockSession({})

    def test_explode(self):
        with self.assertRaises(NotImplementedError):
            self.mocked.session

    def test_ensure_compat(self):
        import companion
        for key in dir(companion.Session):
            if key.startswith('__'):
                # skip special methods etc
                continue

            self.assertIn(key, dir(self.mocked))
