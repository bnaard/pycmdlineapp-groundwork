import copy
from typing import Dict, Any, List, Set


# Original code Copyright Ferry Boender, released under the MIT license.
# Source: https://www.electricmonk.nl/log/2017/05/07/merging-two-python-dictionaries-by-deep-updating/

def deepupdate(target: Dict[Any, Any], source: Dict[Any, Any]):
    """Simple function to deep-update target dictionary with source.
    Non-changeable update strategy: overwrite. 
    For each key, value in source: if key doesn't exist in target, deep-copy it from
    source to target. Otherwise, if value is a list, target[key] is extended with
    source[key]. If value is a set, target[key] is updated with value. If value is a dictionary,
    recursively deep-update it.
    Args:
        target: Dictionary that gets updated.
        source: Dictionary, whose values are updated to target.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print(t)
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for key, value in source.items():
        if isinstance(value, List):
            if not key in target:
                target[key] = copy.deepcopy(value)
            else:
                target[key].extend(value)
        elif isinstance(value, Dict):
            if not key in target:
                target[key] = copy.deepcopy(value)
            else:
                deepupdate(target[key], value)
        elif isinstance(value, Set):
            if not key in target:
                target[key] = value.copy()
            else:
                target[key].update(value.copy())
        else:
            target[key] = copy.copy(value)
