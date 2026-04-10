from __future__ import annotations

from typing import Literal, NamedTuple
from unittest import TestCase

from pytypeinfo import TypeInfo, TypeInfoCollection


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class _ExampleClass(NamedTuple):

    member: int
    other: dict[str, int]
    foo: Literal[1, 2, 3]


class _IncompatibleClass(NamedTuple):

    member: int
    other: dict[str, int]


class _CompatibleClass(NamedTuple):

    member: int
    other: dict[str, int]
    foo: Literal[1, 2, 3]
    extra: str


class TestTypeInfoCollection(TestCase):

    def setUp(self) -> None:
        self._col = TypeInfoCollection(_ExampleClass)

    def test_collection(self):
        for mem in self._col.values():
            assert isinstance(mem, TypeInfo)

        good = _ExampleClass(
            member=1,
            other={'hallo': 1},
            foo=3
        )
        assert self._col.check(good)

        bad = _ExampleClass(
            member=1,
            other={'hallo': 1},
            foo=4                   # type: ignore
        )
        assert not self._col.check(bad)

    def test_other_type(self):

        # Compatible object does not raise exception
        good = _CompatibleClass(
            member=1,
            other={'hallo': 1},
            foo=3,
            extra='Hallo Welt'
        )
        assert self._col.check(good, accept_other=True, do_raise=True)

        # Incompatible object has wrong type
        bad = _IncompatibleClass(
            member=1,
            other={'hallo': 2}
        )
        self.assertRaises(  # noqa: PT027
            TypeError,
            self._col.check,
            bad,
            do_raise=True
        )

        # Incompatible object has missing member
        self.assertRaises(  # noqa: PT027
            KeyError,
            self._col.check,
            bad,
            accept_other=True,
            do_raise=True
        )


if __name__ == '__main__':
    from unittest import main
    main()
