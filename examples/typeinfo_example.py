from __future__ import annotations

from typing import NamedTuple

from pytypeinfo import TypeInfoCollection


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class MyConfig(NamedTuple):
    value: int = 0
    other_value: str = 'Hello World'


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def example() -> None:

    # We create a TypeInfoCollection that contains type information of all 
    # members
    config_type_info = TypeInfoCollection(MyConfig)

    # Type information for each member are available
    print(config_type_info['value'].type)

    # Checking a valid MyConfig instance returns True
    conf_good = MyConfig(value=5, other_value='FooBar')
    print(config_type_info.check(conf_good))

    # Checking an invalid MyConfig instance return False
    conf_bad = MyConfig(value=5.5)
    print(config_type_info.check(conf_bad))


if __name__ == '__main__':
    example()
