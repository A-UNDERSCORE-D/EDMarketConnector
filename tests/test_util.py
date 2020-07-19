
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
