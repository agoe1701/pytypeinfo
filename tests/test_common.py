from __future__ import annotations

from typing import Optional
from unittest import TestCase

from pytypehintcheck import TypeInfo


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class TestCommon(TestCase):

    def assert_type_info(  # noqa: PLR0912, PLR0913
        self,
        tp: TypeInfo,
        call_params: Optional[bool | tuple] = (),
        call_returns: Optional[bool | TypeInfo] = None,
        is_annotation: bool = False,
        is_any: bool = False,
        is_callable: bool = False,
        is_class_var: bool = False,
        is_ellipsis: bool = False,
        is_immutable: bool = False,
        is_literal: bool = False,
        is_mapping: bool = False,
        is_none: bool = False,
        is_sequence: bool = False,
        is_strict: bool = False,
        is_tuple: bool = False,
        is_type: bool = False,
        is_type_var: bool = False,
        is_union: bool = False,
        literal_values: Optional[bool | tuple] = (),
        metadata: Optional[bool | tuple] = (),
        origin: Optional[bool] = None,
        sub_types: Optional[bool | tuple] = (),
        type: Optional[bool] = None
    ) -> None:
        assert isinstance(tp, TypeInfo)

        if isinstance(call_params, bool):
            assert call_params
        else:
            assert tp.call_params == call_params

        if isinstance(call_returns, bool):
            assert call_returns
        else:
            assert tp.call_returns == call_returns

        assert tp.is_annotation == is_annotation
        assert tp.is_any == is_any
        assert tp.is_callable == is_callable
        assert tp.is_class_var == is_class_var
        assert tp.is_ellipsis == is_ellipsis
        assert tp.is_immutable == is_immutable
        assert tp.is_literal == is_literal
        assert tp.is_mapping == is_mapping
        assert tp.is_none == is_none
        assert tp.is_sequence == is_sequence
        assert tp.is_strict == is_strict
        assert tp.is_tuple == is_tuple
        assert tp.is_type == is_type
        assert tp.is_type_var == is_type_var
        assert tp.is_union == is_union

        if isinstance(literal_values, bool):
            assert literal_values
        else:
            assert tp.literal_values == literal_values

        if isinstance(metadata, bool):
            assert metadata
        else:
            assert tp.metadata == metadata

        if isinstance(origin, bool):
            assert origin
        else:
            assert tp.origin == origin

        if isinstance(sub_types, bool):
            assert sub_types
        else:
            assert tp.sub_types == sub_types

        if isinstance(type, bool):
            assert type
        else:
            assert tp.type == type
