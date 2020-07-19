from typing import Dict, Any

import companion


class MockSession(companion.Session):
    """
    A mocked Session class for use with tests that talk to CAPI
    Note that this does NOT do any of the same validation that the real Session does -- its simply here to provide
    repeatable outputs and some basic behaviour copying
    """

    def __init__(self, mock_data: Dict[str, Any]) -> None:
        super().__init__()
        self.mock_data__ = mock_data
        self.auth = MockAuth()
        self.login_ok = True

    def login(self, cmdr: str = None, is_beta: bool = False) -> bool:
        # TODO: step though AUTH states?
        self.state = self.STATE_OK
        self.credentials = {
            'cmdr': cmdr,
            'is_beta': is_beta
        }

        self.server = companion.SERVER_AUTH if not is_beta else companion.SERVER_BETA
        return self.login_ok

    def auth_callback(self) -> None:
        return

    def query(self, endpoint: str = None) -> Dict[str, Any]:
        return self.mock_data__.copy()

    def profile(self):
        return self.query()  # all the data should be in the mocked files

    def station(self):
        return self.query()  # all the data should be in the mocked files

    def close(self):
        self.state = self.STATE_INIT

    def invalidate(self):
        self.close()

    @property
    def session(self):
        raise NotImplementedError("Nothing should be messing with our session")

    @session.setter
    def session(self, _):
        pass  # eat the attempt to set it


class MockAuth:
    """MockAuth mocks out companion.Auth, it mostly throws errors to find things using it that shouldn't"""

    def authorize(self, payload):
        raise NotImplementedError("things other than Session should not use this")

    @staticmethod
    def invalidate(cmdr):
        raise NotImplementedError("things other than Session should not use this")

    def refresh(self):
        raise NotImplementedError("things other than Session should not use this")
