from __future__ import annotations

from typing import Callable, get_type_hints
from unittest import TestCase

from pytypehintcheck import TypeInfo


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class _CallableHints:
    call_simple: Callable[[int, str], bool]
    call_ellipsis: Callable[..., bool]
    call_return_none: Callable[..., None]
    call_no_params: Callable[[], None]


class CallableTests(TestCase):

    def setUp(self) -> None:
        self._hints = get_type_hints(_CallableHints, include_extras=True)
        return super().setUp()

    def test_params_and_return_value(self):
        info = TypeInfo(self._hints['call_simple'])
        assert info.is_callable
        assert len(info.call_params) == 2
        assert info.call_params[0].type is int
        assert info.call_params[1].type is str
        assert info.call_returns.type is bool

        def good(a: int, b: str) -> bool:
            ...

        def bad(a: float, b: str) -> bool:
            ...

        assert info.check(good)
        assert not info.check(bad)

    def test_variable_params_return_value(self):
        info = TypeInfo(self._hints['call_ellipsis'])
        assert info.is_callable
        assert len(info.call_params) == 1
        assert info.call_params[0].is_ellipsis
        assert info.call_returns.type is bool

    def test_no_return(self):
        info = TypeInfo(self._hints['call_return_none'])
        assert info.is_callable
        assert len(info.call_params) == 1
        assert info.call_params[0].is_ellipsis
        assert info.call_returns.is_none

    def test_no_params_no_return(self):
        info = TypeInfo(self._hints['call_no_params'])
        assert info.is_callable
        assert len(info.call_params) == 0
        assert info.call_returns.is_none


if __name__ == '__main__':
    from unittest import main
    main()
