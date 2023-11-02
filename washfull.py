from typing import List

BASE_HP = [50,64,78,92,106,120,134,148,162,338,360,382,404,426,448,470,492,514,536,558,580,602,624,646,668,690,712,734,756,1103,1125,1147,1169,1191,1213,1235,1257,1279,1301,1323,1345,1367,1389,1411,1433,1455,1477,1499,1521,1543,1565,1587,1609,1631,1653,1675,1697,1719,1741,1763,1785,1807,1829,1851,1873,1895,1917,1939,1961,1983,2005,2027,2049,2071,2093,2115,2137,2159,2181,2203,2225,2247,2269,2291,2313,2335,2357,2379,2401,2423,2445,2467,2489,2511,2533,2555,2577,2599,2621,2643,2665,2687,2709,2731,2753,2775,2797,2819,2841,2863,2885,2907,2929,2951,2973,2995,3017,3039,3061,3083,3105,3127,3149,3171,3193,3215,3237,3259,3281,3303,3325,3347,3369,3391,3413,3435,3457,3479,3501,3523,3545,3567,3589,3611,3633,3655,3677,3699,3721,3743,3765,3787,3809,3831,3853,3875,3897,3919,3941,3963,3985,4007,4029,4051,4073,4095,4117,4139,4161,4183,4205,4227,4249,4271,4293,4315,4337,4359,4381,4403,4425,4447,4469,4491,4513,4535,4557,4579,4601,4623,4645,4667,4689,4711,4733,4755,4777,4799,4821,4843]

class Equipment:
    name: str
    level_req: int
    INT: int
    all_equipment: List = []

    def __init__(self, name: str, level: int, INT: int) -> None:
        self.name = name
        self.level_req = level
        self.INT = INT
        Equipment.all_equipment.append(self)

class Player:
    INT: int
    int_goal: int
    level: int
    equipment: List[Equipment]
    maple_warrior_precent: int
    bonus_mana: int
    bonus_HP: int
    mana_cost: int
    HP_gain: int
    fresh_AP: int
    washes: int
    is_washing: int
    stale_ap: int

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
    def HP(self):
        return self.bonus_HP + BASE_HP[self.level - 1]
    
    def __init__(self, int_goal: int, HP_gain: int, mp_cost: int, mw: int) -> None:
        self.level = 1
        self.int_goal = int_goal
        self.equipment = []
        self.HP_gain = HP_gain
        self.mana_cost = mp_cost
        self.bonus_HP = 0
        self.bonus_mana = 0
        self.INT = 10
        self.maple_warrior_precent = mw
        self.fresh_AP = 0
        self.washes = 0
        self.is_washing = True
        self.stale_ap = 0

    def level_up(self):
        self.bonus_mana += self.bonus_mana_on_lvl_up
        self.level += 1
        self.fresh_AP += 5
        # print(f"lvled up to {self.level}")
        self.gear_up()

    def add_int(self):
        if self.INT < self.int_goal:
            self.INT += self.fresh_AP
            self.INT += self.stale_ap
            self.fresh_AP = 0
            self.stale_ap = 0

    def gear_up(self):
        for e in Equipment.all_equipment:
            if e.level_req > self.level:
                continue
            new = True
            for g in self.equipment:
                if e.name == g.name:
                    new = False
                    if e.INT > g.INT:
                        self.equipment.remove(g)
                        self.equipment.append(e)
                        # print(f"equiping: {e.name}")
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
        # print(f"at lvl {self.level} mp wash gain was: {self.bonus_mana - before}")

    def hp_wash(self, max_amount=9999):
        if max_amount > self.bonus_mana / self.mana_cost:
            washes = int(self.bonus_mana / self.mana_cost)
        else:
            washes = max_amount
        for _ in range(washes):
            self.bonus_HP += 16
            self.bonus_mana -= 12
        self.washes += washes


    def progress(self, lvls: int, mana_wash: bool):
        for _ in range(lvls):
            self.level_up()
            if self.is_washing and mana_wash:
                self.mp_wash()
                self.add_int()
                continue
            if self.is_washing:
                self.add_int()
            if mana_wash:
                self.mp_wash()
            

    def fix_char(self):
        self.is_washing = False
        self.washes += self.INT - 4
        self.INT = 4

    def __str__(self) -> str:
        return f"lvl: {self.level} base INT: {self.INT} total INT: {self.total_int} fresh ap: {self.fresh_AP} bonus MP: {self.bonus_mana} bonus HP: {self.bonus_HP} total HP: {self.HP} reset scrolls: {self.washes} cost: {(self.washes) * 3300}nx"


# hat1 = Equipment("hat",22, 5)
# hat2 = Equipment("hat",50, 32)
# #face = Equipment("face", 22, 9)
# ear = Equipment("ear", 15, 8)
# wand = Equipment("wand", 10, 8)
# robe = Equipment("overall", 20, 20)
# pendant1 = Equipment("pendant", 30, 3)
# pendant2 = Equipment("pendant", 50, 5)
# pendant3 = Equipment("pendant", 120, 22)
# shield = Equipment("shield",10,7)
# eye = Equipment("eye", 45, 11)
# cape1 = Equipment("cape", 32, 9)
# cape2 = Equipment("cape", 80, 18)
# shoe = Equipment("shoe", 30, 1)
# gloves = Equipment("glove", 20, 12)
all = Equipment("hat", 20, 80)

ashalNL = Player(360, 16, 12, 10)
ashalSE = Player(165,16,12,10)
AimAssist = Player(360, 16, 12, 10)
AimAssist.progress(70, False)
print(AimAssist)
AimAssist.progress(74, True)
AimAssist.hp_wash()
AimAssist.fix_char()
print(AimAssist)
AimAssist.progress(35, False)
print(AimAssist)

# ashalSE.level = 159
# ashalSE.INT = 550
# ashalSE.progress(21, True)
# print(ashalSE)
# ashalSE.hp_wash()
# print(462 + 10344 + ashalSE.bonus_HP)

# ashalNL.progress(150, False)
# print(ashalNL)
# ashalNL.mp_wash(100)
# print(ashalNL)
# ashalNL.hp_wash()
# print(ashalNL)
# ashalNL.fix_char()
# print(ashalNL)
# ashalNL.progress(25, False)
# print(ashalNL)
# ashalNL.hp_wash()
# print(ashalNL)