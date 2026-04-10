from __future__ import annotations

from typing import Any, Callable, NamedTuple

from pytypeinfo import TypeInfoCollection


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class MyConfig(NamedTuple):
    value: int = 0
    other_value: str = 'Hello World'


class MyTypedClass:

    value: Any
    items: tuple[int, ...]
    callback: Callable[[int], bool]


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def example_config() -> None:

    # We create a TypeInfoCollection that contains type information of all 
    # members
    config_type_info = TypeInfoCollection(MyConfig)

    # Type information for each member are available
    print('value type is int', config_type_info['value'].type)

    # Checking a valid MyConfig instance returns True
    conf_good = MyConfig(value=5, other_value='FooBar')
    print('good config passes', config_type_info.check(conf_good))

    # Checking an invalid MyConfig instance return False
    conf_bad = MyConfig(value=5.5)
    print('bad config fails', config_type_info.check(conf_bad))


def example_inspect() -> None:

    info = TypeInfoCollection(MyTypedClass)

    info_value = info['value']
    print('value can be any value', info_value.is_any)

    info_items = info['items']
    print('items is tuple', info_items.is_tuple)
    print('items is sequence', info_items.is_sequence)
    print('items first type is int', info_items.sub_types[0].type is int)
    print('items can take any number of ints ', info_items.sub_types[1].is_ellipsis)

    info_callback = info['callback']
    print('callback is a callable ', info_callback.is_callable)
    print('callback first parameter is int', info_callback.call_params[0].type is int)
    print('callback returns bool', info_callback.call_returns.type is bool)


if __name__ == '__main__':
    example_config()
    example_inspect()
