from hypothesis.strategies._internal.core import recursive
import pytest
from hypothesis import given, strategies as st
from string import printable
from typing import Dict, Any, List, Tuple
from pycmdlineapp_groundwork.utility.dict_deep_update import (
    dict_deep_update,
    MAX_RECURSION_DEPTH,
)

key_strategies = (
    st.none() | st.booleans() | st.integers() | st.floats() | st.text(printable)
)
value_strategies = (
    st.none()
    | st.booleans()
    | st.integers()
    | st.floats()
    | st.text(printable)
    | st.lists(
        st.none() | st.booleans() | st.integers() | st.floats() | st.text(printable)
    )
    | st.dictionaries(
        st.text(printable),
        st.none() | st.booleans() | st.integers() | st.floats() | st.text(printable),
    )
)


def _determine_should_raise_recursion_exception(element, depth=0):
    result = False
    if isinstance(element, list):
        for item in element:
            result = (
                True
                if _determine_should_raise_recursion_exception(item, depth + 1)
                else False
            )
    elif isinstance(element, dict):
        for _, item in element.items():
            result = (
                True
                if _determine_should_raise_recursion_exception(item, depth + 1)
                else False
            )
    else:
        result = True if depth > MAX_RECURSION_DEPTH else False
    return result


def check_assert_dict(test_case_dict):
    if test_case_dict["target"] is None or test_case_dict["source"] is None:
        with pytest.raises(ValueError):
            merged_dict = test_case_dict["target"]
            dict_deep_update(merged_dict, test_case_dict["source"])
    elif test_case_dict["should_raise_recursion_exception"]:
        with pytest.raises(RecursionError):
            merged_dict = test_case_dict["target"]
            dict_deep_update(merged_dict, test_case_dict["source"])
    else:
        merged_dict = test_case_dict["target"]
        dict_deep_update(merged_dict, test_case_dict["source"])
        assert merged_dict == test_case_dict["result"]


@given(st.data())
def test_dict_deep_update(data):

    k1 = data.draw(key_strategies)
    v1 = data.draw(value_strategies)
    k2 = data.draw(key_strategies)
    v2 = data.draw(value_strategies)
    k3 = data.draw(key_strategies)
    v3 = data.draw(value_strategies)
    vp1 = data.draw(key_strategies)
    vp2 = data.draw(key_strategies)
    vp3 = data.draw(key_strategies)

    test_cases = [
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: v2},
            "source": {k3: v3},
            "result": {k1: v1, k2: v2, k3: v3},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: vp2},
            "source": {k2: vp3},
            "result": {k1: v1, k2: vp3},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: [vp2]},
            "source": {k2: [v2, vp3]},
            "result": {k1: v1, k2: [vp2, v2, vp3]},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: [vp2]},
            "source": {k2: vp3},
            "result": {k1: v1, k2: vp3},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: {k3: vp2} },
            "source": {k2: [v2, vp3]},
            "result": {k1: v1, k2: [v2, vp3]},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: {k3: vp2}},
            "source": {k2: vp3},
            "result": {k1: v1, k2: vp3},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: {k3: vp2}},
            "source": {k2: {k3: vp3}},
            "result": {k1: v1, k2: {k3: vp3}},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {k1: v1, k2: {k3: vp2}},
            "source": {k2: {k2: v3}},
            "result": {k1: v1, k2: {k2: v3, k3: vp2}},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {},
            "source": {},
            "result": {},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {},
            "source": {},
            "result": {},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {},
            "source": {},
            "result": {},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {},
            "source": {},
            "result": {},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {},
            "source": {},
            "result": {},
        },
        {
            "should_raise_recursion_exception": False,
            "target": {},
            "source": {},
            "result": {},
        },
    ]

    for i, test_case in enumerate(test_cases):
        test_cases[i]["should_raise_recursion_exception"] = (
            _determine_should_raise_recursion_exception(test_cases[i]["target"], 0)
            | _determine_should_raise_recursion_exception(test_cases[i]["source"], 0)
            | _determine_should_raise_recursion_exception(test_cases[i]["result"], 0)
        )

        check_assert_dict(test_cases[i])
