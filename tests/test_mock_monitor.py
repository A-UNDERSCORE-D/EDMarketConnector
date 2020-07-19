import unittest
import inspect

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

        for key in EDLogs.__dict__:
            if key.startswith('_'):
                # These are internal, anything accessing them ought to explode anyway
                continue

            assert key in dir(mock_monitor.MockEDLog), NOT_COMPAT + "Missing field {!r}".format(key)

            attr = getattr(EDLogs, key)
            mock_attr = getattr(mock_monitor.EDLogs, key)

            if not callable(attr):
                continue

            assert callable(mock_attr), NOT_COMPAT + "Field {!r} exists but is not callable".format(key)

            orig_params = inspect.signature(attr).parameters
            orig_params = inspect.signature(mock_attr).parameters

            assert len(orig_params) == len(orig_params), \
                NOT_COMPAT + "Signature length for {!r} does not match".format(key)

            for key in orig_params:
                assert orig_params[key] == orig_params[key], \
                    NOT_COMPAT + "signature for {!r} does not match".format(key)

    def test_exploding_properties(self):
        to_test = mock_monitor.MockEDLog()
        with self.assertRaises(test_util.NothingShouldTouchThisException):
            print(to_test.event_queue)
