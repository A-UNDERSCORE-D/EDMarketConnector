from collections import defaultdict
from typing import Any

from mock_companion import MockSession
from monitor import EDLogs
import test_util

DEFAULT_STATE = {
    'Captain': None,  # On a crew
    'Cargo': defaultdict(int),
    'Credits': None,
    'FID': None,  # Frontier Cmdr ID
    'Horizons': None,  # Does this user have Horizons?
    'Loan': None,
    'Raw': defaultdict(int),
    'Manufactured': defaultdict(int),
    'Encoded': defaultdict(int),
    'Engineers': {},
    'Rank': {},
    'Reputation': {},
    'Statistics': {},
    'Role': None,  # Crew role - None, Idle, FireCon, FighterCon
    'Friends': set(),  # Online friends
    'ShipID': None,
    'ShipIdent': None,
    'ShipName': None,
    'ShipType': None,
    'HullValue': None,
    'ModulesValue': None,
    'Rebuy': None,
    'Modules': None,
}


class MockEDLog:
    """
    MockEDLog is a mock version of monitor.EDLogs

    We do not subclass EDLogs because it is a subclass of various file system handlers, and subclassing that may have
    unintended side effects depending on OS etc.
    """

    def __init__(self, state=None, internal_state=None):
        if state is None:
            self.state = DEFAULT_STATE.copy()
        elif isinstance(state, MockSession):
            ...  # TODO: copy the state out of the mock session when setting ourself up
        else:
            self.state = state

        #  copied from the real implementation
        self.version = None
        self.is_beta = False
        self.mode = None
        self.group = None
        self.cmdr = None
        self.planet = None
        self.system = None
        self.station = None
        self.station_marketid = None
        self.stationtype = None
        self.coordinates = None
        self.systemaddress = None
        self.started = None  # This is when the _game_ started

        self._started = False
        self._game_running = internal_state['game_running'] if internal_state is not None else False
        self._ship = internal_state['ship'] if internal_state is not None else None

    @test_util.exploding_property
    def event_queue(self):
        pass

    def start(self):
        self._started = True

    def stop(self):
        self._started = False

    def close(self):
        return

    def running(self):
        return self._started

    def on_created(self):
        return

    def worker(self):
        return

    def canonicalise(self, item: Any) -> str:
        return EDLogs.canonicalise(..., item)  # type: ignore # yes I'm sending None, it doesn't use it

    def category(self, item: Any) -> str:
        return EDLogs.category(..., item)  # type: ignore # yes I'm sending None, it doesn't use it

    @test_util.exploding_property
    def get_entry(self):
        pass

    @test_util.exploding_property
    def parse_entry(self, line):
        return

    def game_running(self):
        return self._game_running

    def ship(self, timestamped=True):
        return self._ship

    def export_ship(self, filename=None):
        return
