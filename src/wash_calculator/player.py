from typing import List

from .equipment import Equipment
from .job import Job


class Player:
    INT: int
    int_goal: int
    level: int
    equipment: List[Equipment]
    maple_warrior_precent: int
    bonus_mana: int
    bonus_HP: int
    fresh_AP: int
    washes: int
    mp_washes: int
    is_adding_int: bool
    is_adding_fresh_ap_into_hp: bool
    stale_ap: int
    name: str
    job: Job
    main_stat: int
    fresh_ap_into_hp_total: int

    @property
    def total_int(self):
        total_int = self.INT
        for e in self.equipment:
            total_int += e.INT
        if self.level > 10:
            return int(total_int * (self.maple_warrior_precent / 100 + 1))
        else:
            return total_int

    @property
    def bonus_mana_on_lvl_up(self): 
        return int(self.total_int / 10)
    
    @property
    def bonus_mana_from_ap(self):
        return int(self.INT / 10)
            

    @property
    def health(self):
        return self.bonus_HP + self.job.base_hp[self.level - 1]
    
    def __init__(self, int_goal: int, job: Job, name: str, mw: int) -> None:
        self.level = 1
        self.int_goal = int_goal
        self.equipment = []
        self.bonus_HP = 0
        self.bonus_mana = 0
        self.INT = 10
        self.maple_warrior_precent = mw
        self.fresh_AP = 0
        self.washes = 0
        self.is_adding_int = True
        self.stale_ap = 0
        self.name = name
        self.job = job
        self.main_stat = 5
        self.is_adding_fresh_ap_into_hp = True
        self.mp_washes = 0
        self.fresh_ap_into_hp_total = 0

    def reset_player(self) -> None:
        self.level = 1
        self.equipment = []
        self.bonus_HP = 0
        self.bonus_mana = 0
        self.INT = 10
        self.fresh_AP = 0
        self.washes = 0
        self.is_adding_int = True
        self.stale_ap = 0
        self.main_stat = 5
        self.mp_washes = 0
        self.is_adding_fresh_ap_into_hp = True
        self.fresh_ap_into_hp_total = 0


    def level_up(self, int_gears: List[Equipment]):
        self.bonus_mana += self.bonus_mana_on_lvl_up
        self.level += 1
        self.fresh_AP += 5
        # print(f"lvled up to {self.level}")
        self.gear_up(int_gears)

    def add_int(self):
        if self.INT < self.int_goal:
            if self.level >= 7 and self.level <=10:
                self.main_stat += self.fresh_AP
                self.INT += self.stale_ap
            else:
                self.INT += self.fresh_AP
                self.INT += self.stale_ap
            self.fresh_AP = 0
            self.stale_ap = 0

    def gear_up(self, int_gears: List[Equipment]):
        for e in int_gears:
            if e.level_req > self.level:
                continue
            new = True
            for g in self.equipment:
                if e.category == g.category:
                    new = False
                    if e.INT > g.INT:
                        self.equipment.remove(g)
                        self.equipment.append(e)
                        # print(f"removing: {g}")
                        # print(f"equiping: {e}")                 
            if new:
                # print(f"equiping: {e.name}")
                self.equipment.append(e)
        
    def mp_wash(self, max_amount=9999):
        before =  self.bonus_mana
        if max_amount > self.fresh_AP:
            washes = self.fresh_AP
        else:
            washes = max_amount
        for _ in range(washes):
            self.bonus_mana += self.bonus_mana_from_ap
        self.fresh_AP -= washes
        self.stale_ap += washes
        self.washes += washes
        self.mp_washes += washes
        # print(f"at lvl {self.level} mp wash gain was: {self.bonus_mana - before}")

    def hp_wash(self, max_amount=9999):
        if max_amount > self.bonus_mana / self.job.mp_cost:
            washes = int(self.bonus_mana / self.job.mp_cost)
        else:
            washes = max_amount
        for _ in range(washes):
            self.bonus_HP += self.job.base_hp_gain
            if self.is_adding_fresh_ap_into_hp and self.level > self.job.hp_gain_skill_level and self.fresh_AP > 0:
                self.fresh_AP -= 1
                self.stale_ap += 1
                self.bonus_HP += self.job.hp_gain_skill
                self.fresh_ap_into_hp_total += 1
            self.bonus_mana -= self.job.mp_cost
        self.washes += washes


    def progress(self, lvls: int, mana_wash: bool, int_gears: List[Equipment]):
        for _ in range(lvls):
            self.level_up(int_gears)
            if self.is_adding_int and mana_wash:
                self.mp_wash()
                self.add_int()
                continue
            if self.is_adding_int:
                self.add_int()
            if mana_wash:
                self.mp_wash()
            

    def fix_char(self):
        self.is_adding_int = False
        self.washes += self.INT - 4
        self.INT = 4

    def copy(self):
        new_guy = Player(self.int_goal, self.job, self.name, self.maple_warrior_precent)
        new_guy.level = self.level
        new_guy.equipment = self.equipment
        new_guy.bonus_HP = self.bonus_HP
        new_guy.bonus_mana = self.bonus_mana
        new_guy.INT = self.INT
        new_guy.fresh_AP = self.fresh_AP
        new_guy.washes = self.washes
        new_guy.is_adding_int = self.is_adding_int
        new_guy.stale_ap = self.stale_ap
        new_guy.main_stat = self.main_stat
        new_guy.is_adding_fresh_ap_into_hp = self.is_adding_fresh_ap_into_hp
        new_guy.mp_washes = self.mp_washes
        new_guy.fresh_ap_into_hp_total = self.fresh_ap_into_hp_total 
        return new_guy

    def __str__(self) -> str:
        return f"name: {self.name} job: {self.job} lvl: {self.level} base INT: {self.INT} total INT: {self.total_int} fresh ap: {self.fresh_AP} bonus MP: {self.bonus_mana} bonus HP: {self.bonus_HP} total HP: {self.health} reset scrolls: {self.washes} cost: {(self.washes) * 3300}nx"
