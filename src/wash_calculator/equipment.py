from typing import List

class Equipment:
    category: str
    name: str
    level_req: int
    INT: int

    def __init__(self, category: str, name: str, level: int, INT: int) -> None:
        self.category = category
        self.name = name
        self.level_req = level
        self.INT = INT

    def __str__(self) -> str:
        return f"{self.category} {self.name} INT: {self.INT} level req: {self.level_req}"
    
    def __repr__(self) -> str:
        return f"<Equipment: {self.category}, {self.name}, INT={self.INT}, level req={self.level_req}>"