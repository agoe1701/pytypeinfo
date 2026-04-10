from __future__ import annotations

from typing import Any, get_type_hints
from unittest import TestCase

from pytypeinfo import TypeInfo


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class _AnyHints:
    foo: Any
    tuple_of_any: tuple[Any, ...]
    dict_of_any: dict[Any, Any]


class MapTests(TestCase):
    """Check the mapping function of the TypeInfo class"""

    def setUp(self) -> None:
        self._hints = get_type_hints(_AnyHints, include_extras=True)

    def test_mapping(self):
        info = TypeInfo(self._hints['foo'])
        items = list(info.items())
        for i, k in enumerate(info):
            assert k == items[i][0]
        assert len(items) == len(info)
        assert info['is_any']


if __name__ == '__main__':
    from unittest import main
    main()
