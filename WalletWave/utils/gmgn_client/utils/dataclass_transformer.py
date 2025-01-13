from typing import Type, TypeVar, List, Dict, Any
from dataclasses import is_dataclass
import dacite

T = TypeVar("T")

def transform(data: Any, dataclass_type: Type[T]) -> T:
    """
    Transforms dict to dataclass

    Args:
        data (Any): The data to transform, either a dict or list of dicts
        dataclass_type (Type[T]): The target dataclass i.e. token_info

    Returns:
        T: A dataclass instance

    Raises:
        ValueError: if type is not a dataclass
        TypeError: if data is not dictionary or list
    """

    if not is_dataclass(dataclass_type):
        raise ValueError(f"{dataclass_type} is not a valid dataclass") # todo enter logging

    if isinstance(data, list):
        return [dacite.from_dict(dataclass_type, item) for item in data]
    elif isinstance(data, dict):
        return dacite.from_dict(dataclass_type, data)
    else:
        raise TypeError(f"Unsupported data type: {type(data)}. Must be a dictionary or list.")