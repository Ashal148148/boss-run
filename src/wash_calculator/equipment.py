from typing import List

class Equipment:
    category: str
    name: str
    level_req: int
    INT: int
    id: int

    def __init__(self, category: str, name: str, level: int, INT: int, id: int = None) -> None:
        self.category = category
        self.name = name
        self.level_req = level
        self.INT = INT
        self.id = id

    def __str__(self) -> str:
        return f"{self.category} {self.name} INT: {self.INT} level req: {self.level_req}"
    
    def __repr__(self) -> str:
        return f"<Equipment: {self.category}, {self.name}, INT={self.INT}, level req={self.level_req}, id={self.id}>"
    
    def __eq__(self, __value: object) -> bool:
        return self.__repr__() == __value.__repr__()