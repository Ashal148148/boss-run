from typing import List, Tuple
from src.wash_calculator.player import Player
from src.wash_calculator.equipment import Equipment
from src.wash_calculator.job import jobs

def do_the_stuff(player: Player,int_gears: List[Equipment], level_goal: int, hp_goal: int) -> Tuple[int,int, int, int, bool]:
    player = player.copy()
    abu_crazy = 20
    abu_step = 10
    success = False
    player.reset_player()
    player.int_goal = abu_crazy
    player.progress(level_goal - 1, False, int_gears) 
    player.mp_wash()  
    first = player.washes
    player.hp_wash()
    second = player.washes
    overwashes = 0
    print(f"ok so the first run cost {first} mana washes, hp reached was {player.health}")
    if player.health >= hp_goal:
        over_hp = int(player.health - hp_goal) 
        over_mp = int(over_hp * player.job.mp_cost / (player.job.base_hp_gain + player.job.hp_gain_skill))
        overwashes = int(over_mp / player.bonus_mana_from_ap)
        if overwashes > first:
            overwashes = first
        print(f"removing {overwashes} overwashes")   
    player.fix_char()
    min_total_cost = first - overwashes + (player.washes - second)
    min_first = first
    min_overwashes = overwashes
    min_abu_crazy = abu_crazy
    max_hp = player.health
    print(f"total cost of washes {min_total_cost}")
    while abu_crazy < 700:
        abu_crazy += abu_step
        player.int_goal = abu_crazy
        player.reset_player()
        player.progress(level_goal - 1, False, int_gears) 
        player.mp_wash()  
        first = player.washes
        player.hp_wash()
        second = player.washes
        overwashes = 0
        if player.health < hp_goal:
            print(f"{abu_crazy}INT: i have failed HP reached was: {player.health}")
        else:
            success = True
        # print(f"ok so the {abu_crazy} INT run cost {first} mana washes, hp reached was {player.health}")
        if player.health >= hp_goal:
            over_hp = int(player.health - hp_goal) 
            over_mp = int(over_hp * player.job.mp_cost / (player.job.base_hp_gain + player.job.hp_gain_skill))
            overwashes = int(over_mp / player.bonus_mana_from_ap)
            if overwashes > first:
                overwashes = first
            print(f"removing {overwashes} overwashes")   
        player.fix_char()
        total_cost = first - overwashes + (player.washes - second)
        print(f"{abu_crazy} INT: total cost of washes {total_cost}")
        if total_cost < min_total_cost or max_hp < player.health and max_hp < hp_goal:
            min_total_cost = total_cost
            min_first = first
            min_overwashes = overwashes
            min_abu_crazy = abu_crazy
            max_hp = player.health
    player.int_goal = min_abu_crazy
    player.reset_player()
    player.progress(level_goal - 1, False, int_gears)
    player.mp_wash()
    bonus_mana = player.bonus_mana
    player.hp_wash()
    player.fix_char()
    best_health = int(player.health - min_overwashes * (min_abu_crazy / 10) * (player.job.base_hp_gain + player.job.hp_gain_skill) / player.job.mp_cost)
    print(f"i have found the best base int: {min_abu_crazy} and it is accompanied by {min_first - min_overwashes} washes, {bonus_mana}")
    return min_abu_crazy, min_first - min_overwashes, best_health, player.washes, success

if __name__ == "__main__":
    int_gears: List[Equipment] = []
    int_gears.append(Equipment("hat",'horns',22, 5))
    int_gears.append(Equipment("hat",'zak',50, 32))
    int_gears.append(Equipment("ear", 'ear',15, 8))
    int_gears.append(Equipment("wand", 'wooden',10, 8))
    int_gears.append(Equipment("overall", 'bathrobe',20, 20))
    int_gears.append(Equipment("pendant", 'yellow muffler',30, 3))
    int_gears.append(Equipment("pendant", 'dep star',50, 5))
    int_gears.append(Equipment("pendant", 'htp', 120, 22))
    int_gears.append(Equipment("shield", 'pan shield',10,7))
    int_gears.append(Equipment("eye", 'raccun',45, 11))
    int_gears.append(Equipment("cape", 'ragged cape', 32, 9))
    int_gears.append(Equipment("cape", 'yellow cape', 50, 12))
    int_gears.append(Equipment("cape", 'cwkpq cape',80, 18))
    int_gears.append(Equipment("shoe", 'slime shoe',30, 1))
    int_gears.append(Equipment("glove", 'red markers', 20, 11))
    player = Player(350, jobs['thief'], 'AshalNL', 10)
    do_the_stuff(player, int_gears, 155, 27885)