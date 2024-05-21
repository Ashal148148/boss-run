from typing import List

class Equipment:
    category: str
    name: str
    level_req: int
    INT: int
    id: int

    categories: list[str] = [
        'Hat',
        'Face Accessory',
        'Eye Accessory',
        'Earring',
        'Overall',
        'Top',
        'Bottom',
        'Shoes',
        'Glove',
        'Weapon',
        'Cape',
        'Pendant',
        'Shield',
        'Ring 1',
        'Ring 2',
        'Ring 3',
        'Ring 4',
        'NX pendant',
        'Extra 1',
        'Extra 2'
    ]

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
    

def battlecat_gears(int_gears: List[Equipment]):
    int_gears.append(Equipment("Hat",'horns',22, 5))
    int_gears.append(Equipment("Hat",'zak',50, 32))
    int_gears.append(Equipment("Earring", 'ear',15, 8))
    int_gears.append(Equipment("Weapon", 'wooden',10, 8))
    int_gears.append(Equipment("Overall", 'bathrobe',20, 20))
    int_gears.append(Equipment("Pendant", 'yellow muffler',30, 3))
    int_gears.append(Equipment("Pendant", 'dep star',50, 5))
    int_gears.append(Equipment("Pendant", 'htp',120, 22))
    int_gears.append(Equipment("Shield", 'pan shield',10,7))
    int_gears.append(Equipment("Eye accessory", 'raccoon',45, 11))
    int_gears.append(Equipment("Cape", 'ragged cape', 32, 9))
    int_gears.append(Equipment("Cape", 'yellow cape', 50, 12))
    int_gears.append(Equipment("Cape", 'cwkpq cape',80, 18))
    int_gears.append(Equipment("Shoes", 'slime shoe',30, 1))
    int_gears.append(Equipment("Glove", 'red markers', 20, 11))
