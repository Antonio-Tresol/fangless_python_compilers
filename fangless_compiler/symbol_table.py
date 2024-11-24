from enum import Enum
from typing import Any


class SymbolData(Enum):
    TYPE = "Type",
    VALUE = "Value",


class SymbolTable:
    def __init__(self):
        self.table: dict[dict] = {}

    def add_name(self, name: str, type: str, value: Any) -> None:
        if name in self.table:
            raise IndexError(f'The name: "{name}" is already defined')
        
        self.table[name] = {SymbolData.TYPE : type,
                            SymbolData.VALUE : value}

    def change_value(self, name: str, new_value_type: str, new_value: Any) -> None:
        if name not in self.table:
            raise IndexError(f'The name: "{name}" is not defined')
        
        if self.table[name][SymbolData.TYPE] != new_value_type:
            raise ValueError(
                f"Name {name} can not change value type from "
                f"{self.table[name][SymbolData.TYPE]} to "
                f"{type(new_value).__name__}"
            )

        
        self.table[name][SymbolData.VALUE] = new_value

    def get_type(self, name: str) -> Any:
        if name not in self.table:
            raise IndexError(f'The name: "{name}" is not defined')
        
        return self.table[name][SymbolData.TYPE]

    def get_value(self, name: str) -> Any:
        if name not in self.table:
            raise IndexError(f'The name: "{name}" is not defined')
        
        return self.table[name][SymbolData.VALUE]
    
    def is_defined(self, name: str) -> bool:
        return name in self.table
    
    def __repr__(self) -> str:
        string = "{\n"
        string += "Symbol Table:\n"
        for name, info in self.table.items():
            string += f"\t{name}: {info},\n"
        string += "}"
        return string
