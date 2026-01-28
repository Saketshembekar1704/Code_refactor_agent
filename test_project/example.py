import os
import sys
from typing import Any, Iterable, List

def calc(x: int, y: int) -> int:
    """calc function.

Args: x, y."""
    result = x + y * 2
    return result if result > 100 else result * 2

class DataProcessor:
    """DataProcessor class."""

    def __init__(self) -> None:
        """__init__ function.

Args: self."""
        self.data: List[Any] = []

    def _normalize_string(self, value: str) -> str:
        """_normalize_string function.

Args: self, value."""
        upper = value.upper()
        return upper[:10] if len(upper) > 10 else upper

    def _normalize_int(self, value: int) -> int:
        """_normalize_int function.

Args: self, value."""
        return value * 2 if value > 0 else 0

    def process_data(self, input_data: Iterable[Any]) -> List[Any]:
        """process_data function.

Args: self, input_data."""
        processed_data: List[Any] = []
        for item in input_data:
            if isinstance(item, str):
                processed_item = self._normalize_string(item)
            elif isinstance(item, int):
                processed_item = self._normalize_int(item)
            else:
                continue
            processed_data.append(processed_item)
        return processed_data

def main() -> None:
    """main function."""
    processor = DataProcessor()
    test_data = ['hello world', 42, -5, 'short']
    result = processor.process_data(test_data)
    print('Processed:', result)
    calc_result = calc(10, 20)
    print('Calc result:', calc_result)
if __name__ == '__main__':
    main()
