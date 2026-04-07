from __future__ import annotations

import collections.abc
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Literal,
    Mapping,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from unittest import TestCase

from pytypehintcheck.type_info import TypeInfo
from pytypehintcheck.typing import Annotated, TypeAlias, get_type_hints


# -----------------------------------------------------------------------------
# Types
# -----------------------------------------------------------------------------

_A = TypeVar('_A')

anno = Annotated[_A, 'Hallo Welt']
CustomInt: TypeAlias = int


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class _TypeInfos:

    def __init__(self, cls: Type[Any]) -> None:
        self._hints = get_type_hints(cls, include_extras=True)

    def __getattr__(self, name: str) -> TypeInfo:
        return TypeInfo(self._hints[name])


class TypeInfoTests(TestCase):

    foo: int
    foo_str: str
    foo_none: None

    tuple_simple: Tuple[Any, ...]
    tuple_args: Tuple[int, str]
    tuple_variadic: Tuple[int, ...]
    tuple_complex: Tuple[int, str, List[int]]

    foo_list: List[int]
    foo_dict: Dict[str, str]
    complex_dict: Dict[str, List[int]]

    mapping: Mapping[str, str]
    sequence: Sequence[str]

    cls_var: ClassVar[float]
    anno_var: anno[int]
    foo_int: CustomInt

    foo_literal: Literal['Hallo', 'Welt', 1, b'ab']
    foo_type_var: _A
    foo_type: Type[int]

    call_simple: Callable[[int, str], bool]
    call_ellipsis: Callable[..., bool]
    call_return_none: Callable[..., None]
    call_no_params: Callable[[], None]

    foo_union: Union[int, str, List[int]]

    def setUp(self) -> None:
        self.infos = _TypeInfos(self.__class__)

    def test_none(self) -> None:

        t_none = TypeInfo(None)
        assert t_none == self.infos.foo_none

    def test_equal(self) -> None:

        t1 = self.infos.foo
        t2 = self.infos.foo_list

        assert t1 != t2
        assert t1 == self.infos.foo
        assert t2 == self.infos.foo_list

    def test_hint_resolve(self) -> None:  # noqa: PLR0915

        foo = self.infos.foo
        assert foo.type is int

        foo_tuple = self.infos.tuple_variadic
        assert len(foo_tuple.sub_types) == 2
        assert foo_tuple.sub_types == (self.infos.foo, TypeInfo(Ellipsis))

        foo_list = self.infos.foo_list
        assert foo_list.type is list
        assert len(foo_list.sub_types) == 1
        assert foo_list.sub_types[0] == self.infos.foo

        foo_dict = self.infos.foo_dict
        assert foo_dict.type is dict
        self.assertTupleEqual(      # noqa
            foo_dict.sub_types,
            (self.infos.foo_str, self.infos.foo_str)
        )

        complex_dict = self.infos.complex_dict
        assert complex_dict.type is dict
        assert len(complex_dict.sub_types) == 2
        assert complex_dict == self.infos.complex_dict

        mapping = self.infos.mapping
        assert mapping.is_mapping
        assert mapping.type == collections.abc.Mapping

        sequence = self.infos.sequence
        assert sequence.is_sequence
        assert sequence.type == collections.abc.Sequence

        cls_var = self.infos.cls_var
        assert cls_var.is_class_var
        assert cls_var.type is float

        anno_var = self.infos.anno_var
        assert anno_var.is_annotation
        assert anno_var.type is int

        foo_int = self.infos.foo_int
        assert foo_int.type is int

        foo_literal = self.infos.foo_literal
        assert foo_literal.literal_values == ('Hallo', 'Welt', 1, b'ab')
        assert foo_literal == self.infos.foo_literal

        foo_type_var = self.infos.foo_type_var
        assert foo_type_var.is_type_var
        assert foo_type_var.type is None

        foo_type = self.infos.foo_type
        assert foo_type.is_type
        assert foo_type.sub_types == (TypeInfo(int),)

        call_simple = self.infos.call_simple
        assert call_simple.is_callable
        assert call_simple.type == collections.abc.Callable
        assert call_simple.call_params == (TypeInfo(int), TypeInfo(str))
        assert call_simple.call_returns == TypeInfo(bool)

        call_ellipsis = self.infos.call_ellipsis
        assert call_ellipsis.is_callable
        assert call_ellipsis.call_params[0].is_ellipsis
        assert call_ellipsis.call_returns == TypeInfo(bool)

        call_return_none = self.infos.call_return_none
        assert call_return_none.is_callable
        assert call_return_none.call_params[0].is_ellipsis
        assert call_return_none.call_returns == TypeInfo(type(None))

        call_no_params = self.infos.call_no_params
        assert call_no_params.is_callable
        assert call_no_params.call_params == ()
        assert call_no_params.call_returns == TypeInfo(type(None))
        assert call_simple != call_ellipsis

        foo_union = self.infos.foo_union
        assert foo_union.is_union
        assert isinstance(1, foo_union.type)
        assert isinstance('hallo', foo_union.type)
        assert isinstance([], foo_union.type)

    def test_simple_check(self) -> None:

        foo_int = self.infos.foo
        assert foo_int.check(1)
        assert not foo_int.check(1.2)

        foo_str = self.infos.foo_str
        assert foo_str.check('Hallo')
        assert foo_str.check('')
        assert not foo_str.check(1)

        foo_union = self.infos.foo_union
        assert foo_union.check(1)
        assert foo_union.check('Hallo')
        assert foo_union.check([])

    def test_tuple_check(self) -> None:

        tuple_simple = self.infos.tuple_simple
        assert tuple_simple.check(())
        assert tuple_simple.check((1, 2, 'lala', [1, 2, 3]))

        # Tuple[int, str]   # noqa
        tuple_args = self.infos.tuple_args
        assert tuple_args.check((1, 'Hallo'))
        assert not tuple_args.check((1, 'Hallo', 1.0))
        assert not tuple_args.check(())
        assert not tuple_args.check((1, 2))

        # Tuple[int, ...]   # noqa
        tuple_variadic = self.infos.tuple_variadic
        assert tuple_variadic.check((1, 2, 3, 4, 5))
        assert tuple_variadic.check(())

        # Tuple[int, str, List[int]]    # noqa
        tuple_complex = self.infos.tuple_complex
        assert tuple_complex.check((1, 'Welt', []))
        assert tuple_complex.check((1, 'Welt', [1, 2, 3]))
        assert not tuple_complex.check((1, 'Welt', [1, 2, 3, 4.0]))
        assert not tuple_complex.check((1, 'Welt'))
        assert not tuple_complex.check((1, 2.0))

    def test_dict_check(self) -> None:

        # Dict[str, str]    # noqa
        foo_dict = self.infos.foo_dict
        assert foo_dict.check({})
        assert foo_dict.check({'hallo': 'welt', 'foo': 'bar'})
        assert not foo_dict.check({'hallo': 'welt', 1: 'bar'})
        assert not foo_dict.check({'hallo': None, 'foo': 'bar'})

        # Dict[str, List[int]]  # noqa
        complex_dict = self.infos.complex_dict
        assert complex_dict.check({})
        assert complex_dict.check({'hallo': []})
        assert complex_dict.check({'hallo': [1, 2, 3]})
        assert complex_dict.check({'hallo': [1, 3], 'foo': [1, 2]})
        assert not complex_dict.check({'hallo': [1, 1.5], 'foo': [2]})

    def test_list_check(self) -> None:

        # List[int]     # noqa
        foo_list = self.infos.foo_list
        assert foo_list.check([])
        assert foo_list.check([1, 2, 3])
        assert not foo_list.check([1, 2, 3, 3.5])

    def test_literal_check(self) -> None:

        # Literal['Hallo', 'Welt', 1, b'ab']    # noqa
        foo_literal = self.infos.foo_literal
        assert foo_literal.check('Hallo')
        assert foo_literal.check('Welt')
        assert foo_literal.check(1)
        assert foo_literal.check(b'ab')
        assert not foo_literal.check(b'abc')
        assert not foo_literal.check(None)

    def test_callable_check(self) -> None:

        # Callable[[int, str], bool]    # noqa
        def good(a: int, b: str) -> bool:
            ...

        def bad(a: float, b: str) -> bool:
            ...

        def bad1() -> bool:
            ...

        def bad2(a: int, b: str) -> int:
            ...

        def bad3(a: int, b: str, c: float) -> bool:
            ...

        def bad4(a: int, b) -> bool:    # noqa
            ...

        def bad5(a: int, b: str) -> None:
            ...

        call_simple = self.infos.call_simple
        assert call_simple.check(good)
        assert not call_simple.check(bad)
        assert not call_simple.check(bad1)
        assert not call_simple.check(bad2)
        assert not call_simple.check(bad3)
        assert not call_simple.check(bad4)
        assert not call_simple.check(bad5)

        # Callable[..., bool]   # noqa
        def good1() -> bool:
            ...

        def no_param_no_return():   # noqa
            ...

        call_ellipsis = self.infos.call_ellipsis
        assert call_ellipsis.check(good)
        assert call_ellipsis.check(good1)
        assert not call_ellipsis.check(bad2)
        assert not call_ellipsis.check(no_param_no_return)

        # Callable[..., None]   # noqa
        call_return_none = self.infos.call_return_none
        assert call_return_none.check(no_param_no_return)
        assert call_return_none.check(bad5)

        # Callable[[], None]    # noqa
        call_no_params = self.infos.call_no_params
        assert call_no_params.check(no_param_no_return)
        assert not call_no_params.check(bad1)


if __name__ == '__main__':
    from unittest import main
    main()
