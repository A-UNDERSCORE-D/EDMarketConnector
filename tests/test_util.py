
import inspect
from typing import Any, ClassVar


class TestingException(Exception):
    pass


class NothingShouldTouchThisException(TestingException):
    """Utility Exception for mocked classes using properties that should "just explode" when accessed"""
    def __init__(self, thing=None, msg=None) -> None:
        default_message = "Nothing should be touching {}".format(thing if thing is not None else "this")

        if msg is not None:
            default_message = msg

        super().__init__(default_message)


def exploding_property(f):
    """exploding_property does what it says on the tin, it makes a property explode if it is used in any way"""

    name = f.__name__

    def explode(name: str, func_type: str):  # technically this is NoReturn, but bare with me
        def actually_explode(*args, **kwargs) -> None:
            raise NothingShouldTouchThisException("{!r} ({})".format(name, func_type))

        return actually_explode

    return property(fget=explode(name, 'setter'), fset=explode(name, 'get'), fdel=explode(name, 'del'), doc=f.__doc__)


def get_name(thing) -> str:
    if inspect.isclass(thing):
        return thing.__name__
    return thing.__class__.__name__


def test_mock_compat(real, mocked, single_underscore=False, double_underscore=False):
    """Compares a mocked object to the real version, ensuring that all fields are the same"""

    NOT_COMPAT = f"mock {get_name(mocked)} is not compatible with {get_name(real)}: "

    for key in real.__dict__:
        if key.startswith('__') and not double_underscore:
            continue
        if key.startswith('_') and not single_underscore:
            # These are internal, anything accessing them ought to explode anyway
            continue

        assert key in dir(mocked), NOT_COMPAT + f"Missing field {key!r}"

        attr = getattr(real, key)
        mock_attr = getattr(mocked, key)

        if not callable(attr):
            continue

        if isinstance(mock_attr, property):
            # Its callable, but its also a property, assume its been overridden in some way on the mock side
            continue

        assert callable(mock_attr), NOT_COMPAT + f"Field {key!r} exists but is not callable"

        orig_params = inspect.signature(attr).parameters
        orig_params = inspect.signature(mock_attr).parameters

        assert len(orig_params) == len(orig_params), NOT_COMPAT + f"Signature length for {key!r} does not match"

        for key in orig_params:
            assert orig_params[key] == orig_params[key], NOT_COMPAT + f"signature for {key!r} does not match"
