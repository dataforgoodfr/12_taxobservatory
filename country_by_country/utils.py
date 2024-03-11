from typing import Any, Dict, Iterable, Tuple
from operator import itemgetter


def pass_values(x):
    if not isinstance(x, list):
        x = [x]
    return {k: itemgetter(k) for k in x}


# Drawn from langchain utils and modified to remove the parent key
def _flatten_dict(
    nested_dict: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Iterable[Tuple[str, Any]]:
    """
    Generator that yields flattened items from a nested dictionary for a flat dict.

    Parameters:
        nested_dict (dict): The nested dictionary to flatten.
        parent_key (str): The prefix to prepend to the keys of the flattened dict.
        sep (str): The separator to use between the parent key and the key of the
            flattened dictionary.

    Yields:
        (str, any): A key-value pair from the flattened dictionary.
    """
    for key, value in nested_dict.items():
        new_key = key
        if isinstance(value, dict):
            yield from _flatten_dict(value, new_key, sep)
        else:
            yield new_key, value


def flatten_dict(
    nested_dict: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Dict[str, Any]:
    """Flattens a nested dictionary into a flat dictionary.

    Parameters:
        nested_dict (dict): The nested dictionary to flatten.
        parent_key (str): The prefix to prepend to the keys of the flattened dict.
        sep (str): The separator to use between the parent key and the key of the
            flattened dictionary.

    Returns:
        (dict): A flat dictionary.

    """
    flat_dict = {k: v for k, v in _flatten_dict(nested_dict, parent_key, sep)}
    return flat_dict
