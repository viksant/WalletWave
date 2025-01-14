from typing import Type, TypeVar, Union, Dict, Any
from dataclasses import is_dataclass, asdict
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

def to_dict(obj: Any, extra_fields: Dict[str, Any] = None, dataclass_type: Type[T] = None) -> Union[Dict[str, Any], T]:
    """
    Converts an object (dataclass or dict) into a dictionary or back to a dataclass with optional additional fields.

    Args:
        obj: The object to convert (dataclass or dictionary).
        extra_fields: Optional additional fields to include in the dictionary.
        dataclass_type: Optionally specify a dataclass type to convert back into a dataclass.

    Returns:
        Union[dict, T]: The converted dictionary with additional fields or a dataclass instance.
    """
    if is_dataclass(obj):
        result = asdict(obj)
    elif isinstance(obj, dict):
        result = obj
    else:
        raise TypeError(f"Unsupported type {type(obj)}. Must be a dataclass or dict.")

    if extra_fields:
        result.update(extra_fields)

    if dataclass_type:
        return dacite.from_dict(dataclass_type, result)

    return result