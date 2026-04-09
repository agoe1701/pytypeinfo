from __future__ import annotations

from typing import Union, get_type_hints

from test_common import TestCommon

from pytypehintcheck import TypeInfo


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class _UnionHints:
    simple: int | str
    old: Union[int, str]


class UnionTests(TestCommon):

    def setUp(self) -> None:
        self._hints = get_type_hints(_UnionHints, include_extras=True)
        return super().setUp()

    def assert_is_union(self, tp: TypeInfo):
        self.assert_type_info(
            tp,
            is_union=True,
            is_type=True,
            type=tp.type is not None,
            sub_types=tp.sub_types is not None
        )

    def test_simple(self):
        info = TypeInfo(self._hints['simple'])

        self.assert_is_union(info)
        assert info.check(5)
        assert info.check('hallo')
        assert not info.check(b'lala')


if __name__ == '__main__':
    from unittest import main
    main()
