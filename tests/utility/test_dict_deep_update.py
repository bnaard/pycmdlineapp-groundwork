from hypothesis.strategies._internal.core import recursive
import pytest
from hypothesis import given, strategies as st
from string import printable
from typing import Dict, Any, List, Tuple
import json
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
value_no_lists_strategies = (
    st.none()
    | st.booleans()
    | st.integers()
    | st.floats()
    | st.text(printable)
    | st.dictionaries(
        st.text(printable),
        st.none() | st.booleans() | st.integers() | st.floats() | st.text(printable),
    )
)



@st.composite
def dict_deep_update_strategy(draw, keys=key_strategies, values=value_strategies, values_no_lists=value_no_lists_strategies):

    k1 = draw(keys)
    v1 = draw(values)
    k2 = draw(keys)
    v2 = draw(values)
    k3 = draw(keys)
    v3 = draw(values)
    vp1 = draw(keys)
    vp2 = draw(keys)
    vp3 = draw(keys)
    vnl1 = draw(values_no_lists)
    vnl2 = draw(values_no_lists)

    return (k1,v1,k2,v2,k3,v3,vp1,vp2,vp3,vnl1,vnl2)



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


def _check_test_case_dict(test_case_dict):
    merged_dict = test_case_dict["target"]
    dict_deep_update(merged_dict, test_case_dict["source"])
    assert merged_dict == test_case_dict["result"]


def _inner_test_dict_deep_merge(test_case_dict):
    test_case_dict["should_raise_recursion_exception"] = (
        _determine_should_raise_recursion_exception(test_case_dict["target"], 0)
        | _determine_should_raise_recursion_exception(test_case_dict["source"], 0)
        | _determine_should_raise_recursion_exception(test_case_dict["result"], 0)
    )
    if test_case_dict["target"] is None or test_case_dict["source"] is None:
        with pytest.raises(ValueError):
            merged_dict = test_case_dict["target"]
            dict_deep_update(merged_dict, test_case_dict["source"])
            return

    if test_case_dict["should_raise_recursion_exception"]:
        with pytest.raises(RecursionError):
            merged_dict = test_case_dict["target"]
            dict_deep_update(merged_dict, test_case_dict["source"])
            return

    _check_test_case_dict(test_case_dict)



@given(dict_keys_values=dict_deep_update_strategy())
def test_dict_deep_update_001(dict_keys_values):
    k1,v1,k2,v2,k3,v3,vp1,vp2,vp3,vnl1,vnl2 = dict_keys_values
    test_case_dict = {
        "should_raise_recursion_exception": False,
        "target": {k1: v1, k2: v2},
        "source": {k3: v3},
        "result": {k1: v1, k2: v2, k3: v3},
    }
    _inner_test_dict_deep_merge(test_case_dict)
    




# @st.composite
# def dict_deep_update_strategy(draw, keys=key_strategies, values=value_strategies, values_no_lists=value_no_lists_strategies):

#     return {
#         "k1": draw(keys),
#         "v1" : draw(values),
#         "k2" : draw(keys),
#         "v2" : draw(values),
#         "k3" : draw(keys),
#         "v3" : draw(values),
#         "vp1" : draw(keys),
#         "vp2" : draw(keys),
#         "vp3" : draw(keys),
#         "vnl1" : draw(values_no_lists),
#         "vnl2" : draw(values_no_lists),
#     }




# @given(dict_keys_values=dict_deep_update_strategy())
# @pytest.mark.parametrize("test_case_dict_json",
# [
#     ("""{
#         "should_raise_recursion_exception": false,
#         "target": {"k1": "v1", "k2": "v2"},
#         "source": {"k3": "v3"},
#         "result": {"k1": "v1", "k2": "v2", "k3": "vp3"}
# }"""),
# ])
# def test_dict_deep_update(test_case_dict_json, dict_keys_values):
#     for example_key,example_value in dict_keys_values.items():
#         test_case_dict_json= test_case_dict_json.replace(f'"{example_key}"', json.dumps(example_value))

#     test_case_dict = json.loads(test_case_dict_json)

#     test_case_dict["should_raise_recursion_exception"] = (
#         _determine_should_raise_recursion_exception(test_case_dict["target"], 0)
#         | _determine_should_raise_recursion_exception(test_case_dict["source"], 0)
#         | _determine_should_raise_recursion_exception(test_case_dict["result"], 0)
#     )
#     if test_case_dict["target"] is None or test_case_dict["source"] is None:
#         with pytest.raises(ValueError):
#             merged_dict = test_case_dict["target"]
#             dict_deep_update(merged_dict, test_case_dict["source"])
#             return

#     if test_case_dict["should_raise_recursion_exception"]:
#         with pytest.raises(RecursionError):
#             merged_dict = test_case_dict["target"]
#             dict_deep_update(merged_dict, test_case_dict["source"])
#             return

#     _check_test_case_dict(test_case_dict)



# @given(dict_keys_values=dict_deep_update_strategy())
# def test_dict_deep_update(dict_keys_values):
#     k1,v1,k2,v2,k3,v3,vp1,vp2,vp3,vnl1,vnl2 = dict_keys_values
# # def test_dict_deep_update(k1,v1,k2,v2,k3,v3,test_dict):
#     # k1,v1,k2,v2,k3,v3,vp1,vp2,vp3,vnl1,vnl2 = dict_keys_values

#     @pytest.mark.parametrize("test_case_dict",
#     [
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: v2},
#             "source": {k3: v3},
#             "result": {k1: v1, k2: v2, k3: v3},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: vp2},
#             "source": {k2: vp3},
#             "result": {k1: v1, k2: vp3},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: [vp2]},
#             "source": {k2: [v2, vp3]},
#             "result": {k1: v1, k2: [vp2, v2, vp3]},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: [vp2]},
#             "source": {k2: vp3},
#             "result": {k1: v1, k2: vp3},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: {k3: vp2} },
#             "source": {k2: [v2, vp3]},
#             "result": {k1: v1, k2: [v2, vp3]},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: {k3: vp2}},
#             "source": {k2: vp3},
#             "result": {k1: v1, k2: vp3},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: {k3: vp2}},
#             "source": {k2: {k3: vp3}},
#             "result": {k1: v1, k2: {k3: vp3}},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: {k3: vp2}},
#             "source": {k2: {k2: v3}},
#             "result": {k1: v1, k2: {k3: vp2, k2: v3}},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {k1: v1, k2: vnl1},
#             "source": {k2: vnl2},
#             "result": {k1: v1, k2: vnl2},
#         }),
#         ({
#             "should_raise_recursion_exception": False,
#             "target": {},
#             "source": {},
#             "result": {},
#         }),
#     ])
#     def test_inner(test_case_dict):
#         test_case_dict["should_raise_recursion_exception"] = (
#                 _determine_should_raise_recursion_exception(test_case_dict["target"], 0)
#                 | _determine_should_raise_recursion_exception(test_case_dict["source"], 0)
#                 | _determine_should_raise_recursion_exception(test_case_dict["result"], 0)
#             )
#         if test_case_dict["target"] is None or test_case_dict["source"] is None:
#             with pytest.raises(ValueError):
#                 merged_dict = test_case_dict["target"]
#                 dict_deep_update(merged_dict, test_case_dict["source"])
#                 return

#         if test_case_dict["should_raise_recursion_exception"]:
#             with pytest.raises(RecursionError):
#                 merged_dict = test_case_dict["target"]
#                 dict_deep_update(merged_dict, test_case_dict["source"])
#                 return

#         _check_test_case_dict(test_case_dict)


    # test_cases = [
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: v2},
    #         "source": {k3: v3},
    #         "result": {k1: v1, k2: v2, k3: v3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: vp2},
    #         "source": {k2: vp3},
    #         "result": {k1: v1, k2: vp3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: [vp2]},
    #         "source": {k2: [v2, vp3]},
    #         "result": {k1: v1, k2: [vp2, v2, vp3]},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: [vp2]},
    #         "source": {k2: vp3},
    #         "result": {k1: v1, k2: vp3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2} },
    #         "source": {k2: [v2, vp3]},
    #         "result": {k1: v1, k2: [v2, vp3]},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2}},
    #         "source": {k2: vp3},
    #         "result": {k1: v1, k2: vp3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2}},
    #         "source": {k2: {k3: vp3}},
    #         "result": {k1: v1, k2: {k3: vp3}},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2}},
    #         "source": {k2: {k2: v3}},
    #         "result": {k1: v1, k2: {k3: vp2, k2: v3}},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: vnl1},
    #         "source": {k2: vnl2},
    #         "result": {k1: v1, k2: vnl2},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    # ]

    # for i, test_case_dict in enumerate(test_cases):
    #     test_case_dict["index"] = i
    #     test_case_dict["should_raise_recursion_exception"] = (
    #             _determine_should_raise_recursion_exception(test_case_dict["target"], 0)
    #             | _determine_should_raise_recursion_exception(test_case_dict["source"], 0)
    #             | _determine_should_raise_recursion_exception(test_case_dict["result"], 0)
    #         )
    #     if test_case_dict["target"] is None or test_case_dict["source"] is None:
    #         with pytest.raises(ValueError):
    #             merged_dict = test_case_dict["target"]
    #             dict_deep_update(merged_dict, test_case_dict["source"])
    #             return

    #     if test_case_dict["should_raise_recursion_exception"]:
    #         with pytest.raises(RecursionError):
    #             merged_dict = test_case_dict["target"]
    #             dict_deep_update(merged_dict, test_case_dict["source"])
    #             return

    #     _check_test_case_dict(test_case_dict)





    # k1 = data.draw(key_strategies)
    # v1 = data.draw(value_strategies)
    # k2 = data.draw(key_strategies)
    # v2 = data.draw(value_strategies)
    # k3 = data.draw(key_strategies)
    # v3 = data.draw(value_strategies)
    # vp1 = data.draw(key_strategies)
    # vp2 = data.draw(key_strategies)
    # vp3 = data.draw(key_strategies)

    # test_cases = [
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: v2},
    #         "source": {k3: v3},
    #         "result": {k1: v1, k2: v2, k3: v3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: vp2},
    #         "source": {k2: vp3},
    #         "result": {k1: v1, k2: vp3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: [vp2]},
    #         "source": {k2: [v2, vp3]},
    #         "result": {k1: v1, k2: [vp2, v2, vp3]},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: [vp2]},
    #         "source": {k2: vp3},
    #         "result": {k1: v1, k2: vp3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2} },
    #         "source": {k2: [v2, vp3]},
    #         "result": {k1: v1, k2: [v2, vp3]},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2}},
    #         "source": {k2: vp3},
    #         "result": {k1: v1, k2: vp3},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2}},
    #         "source": {k2: {k3: vp3}},
    #         "result": {k1: v1, k2: {k3: vp3}},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {k1: v1, k2: {k3: vp2}},
    #         "source": {k2: {k2: v3}},
    #         "result": {k1: v1, k2: {k2: v3, k3: vp2}},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    #     {
    #         "should_raise_recursion_exception": False,
    #         "target": {},
    #         "source": {},
    #         "result": {},
    #     },
    # ]

    # for i, test_case in enumerate(test_cases):
    #     test_cases[i]["should_raise_recursion_exception"] = (
    #         _determine_should_raise_recursion_exception(test_cases[i]["target"], 0)
    #         | _determine_should_raise_recursion_exception(test_cases[i]["source"], 0)
    #         | _determine_should_raise_recursion_exception(test_cases[i]["result"], 0)
    #     )

    #     check_assert_dict(test_cases[i])
