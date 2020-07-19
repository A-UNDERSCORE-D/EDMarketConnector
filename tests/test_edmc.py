import json
import unittest
import io
import sys
from unittest.mock import patch

from mock_companion import MockSession


class TestEDMC(unittest.TestCase):
    def setUp(self):
        with open("tests/DOCKED-Shinrarta-Dezhra.Jameson Memorial.2020-07-13T23.54.52.json") as f:
            data = json.load(f)

        self.mockSession = MockSession(data)

        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

        self.patches = (
            patch.multiple("sys", stdout=self.stdout, stderr=self.stderr),  # TODO: these appear unclearable
            patch("companion.session", new=self.mockSession),
            patch("sys.argv", sys.argv[:1]),
            patch('monitor.monitor')
        )

        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def clear_listeners(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)
        self.stderr.seek(0)
        self.stderr.truncate(0)

    def test_simple(self):
        try:
            import EDMC  # noqa: F401
        except Exception as e:
            print(f"caught exception: {e}")

        except SystemExit:
            print("caught SystemExit")

        print(f"{self.stdout.getvalue()}")
        print("--------------")
        print(f"{self.stderr.getvalue()}")

        self.clear_listeners()
