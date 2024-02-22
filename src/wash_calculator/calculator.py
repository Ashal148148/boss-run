from typing import List, Tuple
from src.wash_calculator.player import Player
from src.wash_calculator.equipment import Equipment
from src.wash_calculator.job import jobs

def do_the_stuff(player: Player,int_gears: List[Equipment], level_goal: int, hp_goal: int) -> Tuple[int,int, int, int, bool]:
    player = player.copy()
    base_int = 10
    base_int_increment = 10
    success = False
    player.reset_player()
    player.int_goal = base_int
    player.progress(level_goal - 1, False, int_gears)
    player.hp_wash(health_goal=hp_goal)
    while player.fresh_AP and player.health < hp_goal:
        player.mp_wash(1)
        player.hp_wash(health_goal=hp_goal)
    mp_washes = player.mp_washes    
    total_washes = player.washes
    
    print(f"ok so the first run cost {mp_washes} mana washes, hp reached was {player.health}")
    player.fix_char()
    min_total_cost = mp_washes + player.washes - total_washes
    min_mp_washes = mp_washes
    min_base_int = base_int
    min_total_washes = total_washes
    max_hp = player.health
    while base_int < 700:
        base_int += base_int_increment
        player.int_goal = base_int
        player.reset_player()
        player.progress(level_goal - 1, False, int_gears) 
        player.hp_wash(health_goal=hp_goal)
        while player.fresh_AP and player.health < hp_goal:
            player.mp_wash(1)
            player.hp_wash(health_goal=hp_goal)
        mp_washes = player.mp_washes
        total_washes = player.washes
        if player.health < hp_goal:
            pass
            print(f"{base_int}INT: i have failed HP reached was: {player.health}")
        else:
            success = True
        player.fix_char()
        total_cost = mp_washes + (player.washes - total_washes)
        print(f"{player.name} with {base_int} INT: total cost of washes {total_cost}")
        if total_cost < min_total_cost or max_hp < player.health and max_hp < hp_goal:
            min_total_washes = total_washes
            min_total_cost = total_cost
            min_mp_washes = mp_washes
            min_base_int = base_int
            max_hp = player.health
    player.int_goal = min_base_int
    player.reset_player()
    player.progress(level_goal - 1, False, int_gears)
    player.hp_wash(health_goal=hp_goal)
    while player.fresh_AP and player.health < hp_goal:
        player.mp_wash(1)
        player.hp_wash(health_goal=hp_goal)
    player.fix_char()
    best_health = player.health
    print(f"[{player.name}] i have found the best base int: {min_base_int} and it is accompanied by {min_mp_washes} points into MP and {min_total_washes - min_mp_washes} Washes")
    return min_base_int, min_mp_washes, best_health, player.washes, success, player.fresh_ap_into_hp_total, (min_total_washes - min_mp_washes)

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
    int_gears.append(Equipment("eye", 'raccoon',45, 11))
    int_gears.append(Equipment("cape", 'ragged cape', 32, 9))
    int_gears.append(Equipment("cape", 'yellow cape', 50, 12))
    int_gears.append(Equipment("cape", 'cwkpq cape',80, 18))
    int_gears.append(Equipment("shoe", 'slime shoe',30, 1))
    int_gears.append(Equipment("glove", 'red markers', 20, 11))
    player = Player(350, jobs['Thief'], 'AshalNL', 10)
    do_the_stuff(player, int_gears, 155, 27885)