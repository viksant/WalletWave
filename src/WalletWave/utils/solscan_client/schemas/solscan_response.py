from dataclasses import dataclass
from typing import TypeVar, Generic, Type, List

T = TypeVar("T")

@dataclass
class SolscanResponse(Generic[T]):
    success: bool
    data: List[T]

    @staticmethod
    def from_dict(obj: dict, data_class: Type[T]) -> 'SolscanResponse[T]':
        return SolscanResponse(
            success=bool(obj["success"]),
            data=[data_class.from_dict(item) for item in obj["data"]],
        )
