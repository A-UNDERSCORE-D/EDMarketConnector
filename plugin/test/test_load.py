"""Testing suite for plugin loading system."""
import pathlib
import sys
from contextlib import nullcontext
from typing import ContextManager

import pytest

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from plugin.manager import (  # noqa: E402 # Cant be at the top
    PluginDoesNotExistException, PluginHasNoPluginClassException, PluginLoadingException, PluginManager
)


def _idfn(test_data) -> str:
    if isinstance(test_data, pathlib.Path):
        return test_data.parts[-1]

    return ""


current_path = pathlib.Path.cwd() / "plugin/test/test_plugins"

TESTS = [
    (current_path / "good", nullcontext()),
    (current_path / "bad/no_plugin", pytest.raises(PluginHasNoPluginClassException)),
    (current_path / "bad/error", pytest.raises(PluginLoadingException, match="This doesn't load")),
    (current_path / "bad/class_init_error", pytest.raises(PluginLoadingException, match="Exception in init")),
    (current_path / "bad/class_load_error", pytest.raises(PluginLoadingException, match="Exception in load")),
    (current_path / "bad/no_exist", pytest.raises(PluginDoesNotExistException)),
]


@pytest.fixture
def plugin_manager():
    """Provide a PluginManager as a fixture."""
    yield PluginManager()


@pytest.mark.parametrize('path,context',    TESTS,    ids=_idfn)
def test_load(plugin_manager: PluginManager, context: ContextManager, path: pathlib.Path) -> None:
    """
    Test that plugins load as expected.

    :param plugin_manager: a plugin.PluginManager instance to run tests against
    :param context: Context manager to run the test in, pytest.raises is used to assert that an exception is raised
    :param path: [description]
    """
    with context:
        plugin_manager.load_plugin(path)
