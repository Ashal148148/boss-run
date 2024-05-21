from typing import List, Tuple
from src.wash_calculator.player import Player
from src.wash_calculator.equipment import Equipment
from src.wash_calculator.job import jobs

def do_the_stuff(player: Player, int_gears: List[Equipment], level_goal: int, hp_goal: int) -> Tuple[int, int, int, int, bool]:
    player = player.copy()
    base_int = 10
    base_int_increment = 10
    success = False
    player.reset_player()
    player.int_goal = base_int
    player.progress(level_goal - 1, int_gears)
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
        player.progress(level_goal - 1, int_gears) 
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
    player.progress(level_goal - 1, int_gears)
    player.hp_wash(health_goal=hp_goal)
    while player.fresh_AP and player.health < hp_goal:
        player.mp_wash(1)
        player.hp_wash(health_goal=hp_goal)
    player.fix_char()
    best_health = player.health
    print(f"[{player.name}] i have found the best base int: {min_base_int} and it is accompanied by {min_mp_washes} points into MP and {min_total_washes - min_mp_washes} Washes")
    return min_base_int, min_mp_washes, best_health, player.washes, success, player.fresh_ap_into_hp_total, (min_total_washes - min_mp_washes)


def reach_the_goal_no_matter_what(player: Player, int_gears: List[Equipment], level_goal: int, hp_goal: int):
    base_int, points_into_mp, best_health, washes, success, fresh_ap_into_hp_total, points_taken_out_of_mp = do_the_stuff(player, int_gears, level_goal, hp_goal)
    if success:
        return base_int, points_into_mp, best_health, washes, success, fresh_ap_into_hp_total, points_taken_out_of_mp, base_int
    else:
        missing_health = hp_goal - best_health
        missing_mp = int(missing_health / player.job.base_hp_gain) * player.job.mp_cost
        mp_wash_starting_int = base_int
        generated_mp = 0
        while mp_wash_starting_int > (50 + fresh_ap_into_hp_total) and generated_mp < missing_mp:
            mp_wash_starting_int -= 1
            points_into_mp += 1
            washes += 1
            points_taken_out_of_mp += 1
            generated_mp += (mp_wash_starting_int / 10 - 2)  # minus 2 because of the 2 mp tax per fresh ap
        washes += int(generated_mp / player.job.mp_cost)
        best_health += int(generated_mp / player.job.mp_cost) * player.job.base_hp_gain
        success = generated_mp >= missing_mp
        print(f'missing mp {missing_mp} missing hp {missing_health} generated_mp {generated_mp} generated hp {int(generated_mp / player.job.mp_cost) * player.job.base_hp_gain}')
        return base_int, points_into_mp, best_health, washes, success, fresh_ap_into_hp_total, points_taken_out_of_mp, mp_wash_starting_int


def mage_mp_wash_planner(player: Player, int_gears: List[Equipment], level_goal: int, mp_goal: int):
    start_level = 20
    level_increment = 1
    player = player.copy()
    success = False
    player.reset_player()
    player.int_goal = 1100
    player.progress(start_level, int_gears)
    player.is_mp_wash_before_int = True
    while player.level < level_goal:
        if player.level < start_level:
            player.is_mp_wash_before_int = True
        player.progress(1, int_gears)        
        if player.mana >= mp_goal:
            success = True
            player.is_mp_wash_before_int = False
    ideal_mp_washes = player.mp_washes
    ideal_start_level = start_level
    ideal_total_mana = player.mana
    while start_level < level_goal:
        sub_success = False
        player.reset_player()
        player.progress(start_level, int_gears)
        player.is_mp_wash_before_int = True
        while player.level < level_goal:
            player.progress(1, int_gears)        
            if player.mana >= mp_goal:
                success = True
                sub_success = True
                player.is_mp_wash_before_int = False
        if sub_success:
            ideal_mp_washes = player.mp_washes
            ideal_start_level = start_level
            ideal_total_mana = player.mana
        # print(f'[{player.name}] starting at lvl {start_level} has {sub_success} washes: {player.mp_washes} total mana: {player.mana}') 
        start_level += level_increment
    print(f'[{player.name}] final results are {success} starting level: {ideal_start_level} washes: {ideal_mp_washes} total mana: {ideal_total_mana}')
    return ideal_start_level, ideal_mp_washes, ideal_total_mana, success


def mage_hp_wash_planner(player: Player, int_gears: List[Equipment], level_goal: int, hp_goal: int, mp_goal: int):
    base_health_at_goal = player.job.base_hp[level_goal - 1]
    bonus_mana_needed = int((hp_goal - base_health_at_goal) / 6) * 30
    print(f"planning to hp wash mage will need: {bonus_mana_needed} bonus mana")
    start_level, mp_washes, total_mana, is_successful = mage_mp_wash_planner(player, int_gears, level_goal, mp_goal + bonus_mana_needed)
    if is_successful:
        points_reset_from_mp_to_hp = int((hp_goal - base_health_at_goal) / 6)
    else:
        points_reset_from_mp_to_hp = int((total_mana - mp_goal) / 30)
    print()
    total_washes = points_reset_from_mp_to_hp + mp_washes
    total_hp = base_health_at_goal + points_reset_from_mp_to_hp * 6
    total_mana -= points_reset_from_mp_to_hp * 30
    return start_level, total_washes, total_hp, total_mana, is_successful


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
    # player = Player(jobs['Archer/Thief'], 'AshalNL', 10)
    # do_the_stuff(player, int_gears, 155, 27885)
    player = Player(jobs['Mage'], 'Higashi', 10)
    mage_mp_wash_planner(player, int_gears, 180, 42000)