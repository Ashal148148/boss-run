from pydantic import BaseModel

class PlayerSchema(BaseModel):
    INT: int
    int_goal: int
    level: int
    maple_warrior_percent: int
    bonus_mana: int
    bonus_HP: int
    fresh_AP: int
    washes: int
    mp_washes: int
    is_adding_int: bool
    is_adding_fresh_ap_into_hp: bool
    stale_ap: int
    name: str
    job: str
    main_stat: int
    fresh_ap_into_hp_total: int
    id: int

    class Config:
        from_attributes = True