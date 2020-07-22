import unittest

import mock_monitor
from monitor import EDLogs
import test_util

NOT_COMPAT = "MockEDLog is not compatible with monitor.EDLog: "


class TestMockEDLog(unittest.TestCase):
    def test_ensure_compat(self):
        """
        Ensures that MockEDLogs and EDLogs are 100% the same (or the mock is a superset) when it comes to fields and
        that all methods are matched exactly (this may change to ignore annotations if they are added)
        """
        to_test = EDLogs()

        for key in to_test.state:
            self.assertIn(key, mock_monitor.DEFAULT_STATE)

        test_util.test_mock_compat(EDLogs, mock_monitor.MockEDLog)

    def test_exploding_properties(self):
        to_test = mock_monitor.MockEDLog()
        with self.assertRaises(test_util.NothingShouldTouchThisException):
            print(to_test.event_queue)
