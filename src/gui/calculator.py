from functools import partial
from typing import Annotated, Callable, Dict, List
from fastapi import Cookie, Request, Depends
from nicegui import app, ui
import nicegui
from ..identity import accept_user
from src.crud import equipment_crud, player_crud, ResouceNotFoundException
from sqlalchemy.orm import Session
from .dependencies import get_session
from ..schemas import PlayerSchema
from ..wash_calculator import Player, jobs, Equipment, do_the_stuff

print('loading calculator for the first time')

@ui.page('/')
def calculator(request: Request, session: Session = Depends(get_session)) -> None:
    user_id = accept_user(request, session)
    try: 
        player = PlayerSchema.model_validate(player_crud.read_by_user_id(session, user_id), from_attributes=True).model_dump()
        player['job'] = jobs[player['job']]
        player = Player(**player)
    except ResouceNotFoundException:
        player = Player(350, jobs['Thief'], 'AshalNL', 10)
    gears_from_db = equipment_crud.read_by_session_id(session, user_id)
    page_manager: Dict[str, Player | str, List[Player]] = {'active_player': player, 'standby': []}
    int_gears: List[Equipment] = []
    for g, in gears_from_db:
        int_gears.append(Equipment(g.catagory, g.name, g.level_requirement, g.INT, g.id))
    page_manager["active_player"].gear_up(int_gears)
    ui.label("Welcome to BattleCat's HP washing calculator (you might have to scroll down a bit)")
    ui.label("Before we begin ill need some info from you")
    with ui.card():
        name = ui.input("name", placeholder='')
        INT_goal = ui.number(label='Base INT goal')
        ui.label("class: ")
        jobs_display = {1: "Thief" , 2: "Archer", 3: "Brawler", 4: "Gunslinger", 5: "Hero/Paladin", 6: "Spearman"}
        job = ui.select(jobs_display)
        mw = ui.number(label="Maple warrior %")
        def on_click_lets_go(e):
            if INT_goal.value and jobs[jobs_display[job.value]] and name.value and mw.value is not None:
                page_manager["active_player"]=Player(INT_goal.value, jobs[jobs_display[job.value]], name.value, mw.value)
                player_crud.save(session=session ,user_id=user_id, player=page_manager["active_player"])
                print(page_manager['active_player'])
                player_card.refresh()
            else:
                ui.notify("please make sure to fill all fields")
        ui.button("let's go", on_click=on_click_lets_go) 
    with ui.expansion('Gears registration').classes('w-full'):
        ui.label("please register the int gears you plan on using (clicking the GEARS button will ephemerally register my gears)")
        eq_category = ui.input('category')
        eq_name = ui.input('name')
        eq_lvl_req = ui.number('level requirement')
        eq_INT = ui.number('INT')

        def fun():
            int_gears.append(Equipment("hat",'horns',22, 5))
            int_gears.append(Equipment("hat",'zak',50, 32))
            int_gears.append(Equipment("ear", 'ear',15, 8))
            int_gears.append(Equipment("wand", 'wooden',10, 8))
            int_gears.append(Equipment("overall", 'bathrobe',20, 20))
            int_gears.append(Equipment("pendant", 'yellow muffler',30, 3))
            int_gears.append(Equipment("pendant", 'dep star',50, 5))
            int_gears.append(Equipment("pendant", 'htp',120, 22))
            int_gears.append(Equipment("shield", 'pan shield',10,7))
            int_gears.append(Equipment("eye", 'raccun',45, 11))
            int_gears.append(Equipment("cape", 'ragged cape', 32, 9))
            int_gears.append(Equipment("cape", 'yellow cape', 50, 12))
            int_gears.append(Equipment("cape", 'cwkpq cape',80, 18))
            int_gears.append(Equipment("shoe", 'slime shoe',30, 1))
            int_gears.append(Equipment("glove", 'red markers', 20, 11))
            gears_carousel.refresh()

        def add_gear():
            if eq_category.value and eq_name.value and eq_lvl_req.value and eq_INT.value:
                new_gear = equipment_crud.create(session, request.session["id"], eq_category.value, eq_name.value, int(eq_lvl_req.value), int(eq_INT.value))
                int_gears.append(Equipment(eq_category.value, eq_name.value, int(eq_lvl_req.value), int(eq_INT.value), new_gear.id))                    
                gears_carousel.refresh()
            else:
                ui.notify("please make sure to fill all fields")

        ui.button("gears", on_click=fun)
        ui.button("add gear", on_click=add_gear)
        gears_carousel(int_gears, session)              
    
    ui.separator()
    ui.label('This feature will calculate the NX cheapest way to wash your character to your HP goal given your gears')
    with ui.row():
        hp_goal = ui.number('HP goal')
        lvl_goal = ui.number('level goal')
        def on_calculate_click():
            base_int, washes, health, total_resets, success, fresh_ap_into_hp, total_washes = do_the_stuff(page_manager['active_player'], int_gears, int(lvl_goal.value), int(hp_goal.value))
            da_thing_results(int(lvl_goal.value), int(hp_goal.value), base_int, washes, health, total_resets, success, fresh_ap_into_hp, total_washes)
            da_thing_results.refresh()
        ui.button('do the thing', on_click=on_calculate_click)
    ui.separator()
    with ui.row():
        levels = ui.number('levels:', value=1, max=199, min=1)
        def level_up():
            page_manager["active_player"].progress(int(levels.value), False, int_gears)
            player_card.refresh()
        ui.button("Level Up", on_click=level_up)
        def on_toggle_add_int():
            page_manager["active_player"].is_adding_int = not page_manager["active_player"].is_adding_int
        ui.checkbox('Add INT', value=page_manager["active_player"].is_adding_int, on_change=on_toggle_add_int)
        mana_washes = ui.number('washes', value=1, min=1)
        def mana_wash():
            page_manager["active_player"].mp_wash(int(mana_washes.value))
            player_card.refresh()
        ui.button('Mana wash', on_click=mana_wash).tooltip('add fresh AP into MP, Remove the same amount of AP from MP and add it to the main stat')
        def on_toggle_fresh_ap_into_int():
            page_manager["active_player"].is_adding_fresh_ap_into_hp = not page_manager["active_player"].is_adding_fresh_ap_into_hp
        ui.checkbox('Add fresh AP into HP', value=page_manager["active_player"].is_adding_fresh_ap_into_hp, on_change=on_toggle_fresh_ap_into_int).tooltip('Relevant only if your class has an HP growth related skill')
        hp_washes = ui.number('washes', value=1, min=1)
        def hp_wash():
            page_manager["active_player"].hp_wash(int(hp_washes.value))
            player_card.refresh()
        ui.button('HP wash', on_click=hp_wash).tooltip('Reset points from MP into HP')
        def full_hp_wash():
            page_manager["active_player"].hp_wash()
            player_card.refresh()
        ui.button('Reset all bonus mp into hp', on_click=full_hp_wash).classes('red')
        def reset_INT():
            page_manager["active_player"].fix_char()
            player_card.refresh()
        ui.button('Reset INT', on_click=reset_INT).classes('red')
        with ui.dialog() as dialog, ui.card():
            gear_display(page_manager["active_player"].equipment)
            ui.button('close', on_click=dialog.close)
        def on_show_gear():
            gear_display.refresh()
            dialog.open()
        ui.button('Show equiped gear', on_click=on_show_gear)
    player_card(page_manager, int_gears, session, user_id)
    
    ui.label("found a bug? contact me via discord: shaul_carvalho")
    ui.label("donations would be appreciated <todo>")
            


@ui.refreshable
def gears_carousel(int_gears: List[Equipment], session: Session):
    gear_tabs = []
    with ui.tabs().classes('w-half') as tabs:
        for gear in int_gears:
            gear_tabs.append(ui.tab(gear.name))
    if gear_tabs:
        with ui.tab_panels(tabs, value=gear_tabs[0]):
            for t, gear in zip(gear_tabs, int_gears):             
                def on_click_remove(int_gearz, gearz):
                    int_gearz.remove(gearz)
                    equipment_crud.delete(session, gearz.id)
                    gears_carousel.refresh()
                p = partial(on_click_remove, int_gears, gear)
                with ui.tab_panel(t):
                    ui.label(f"category: {gear.category}")
                    ui.label(f"name: {gear.name}")
                    ui.label(f"level requirement: {gear.level_req}")
                    ui.label(f"INT: {gear.INT}")
                    ui.button(f'x', color='red', on_click=p)


@ui.refreshable
def player_card(page_manager: Dict[str, Player], int_gears: List[Equipment], session: Session, user_id: int):
    if user_id:
        player_crud.save(session, user_id, page_manager['active_player'])
    with ui.element('div').classes('p-2 bg-blue-100'):
        ui.label(page_manager['active_player'].name)
        ui.label(f"level: {page_manager['active_player'].level}")
        ui.label(f"job: {page_manager['active_player'].job.name}")
        ui.label(f"Base INT goal: {page_manager['active_player'].int_goal}")
        ui.label(f"Base INT: {page_manager['active_player'].INT}")
        ui.label(f"Total INT: {page_manager['active_player'].total_int}")        
        ui.label(f"Bonus mana: {page_manager['active_player'].bonus_mana}")
        ui.label(f"Bonus health: {page_manager['active_player'].bonus_HP}")
        ui.label(f"Total health: {page_manager['active_player'].health}")
        ui.label(f"Fresh AP: {page_manager['active_player'].fresh_AP}")
        ui.label(f"Stale AP: {page_manager['active_player'].stale_ap}")
        ui.label(f"Main stat: {page_manager['active_player'].main_stat}")
        ui.label(f"Fresh AP added to mana: {page_manager['active_player'].mp_washes}")
        ui.label(f"Fresh AP added to health: {page_manager['active_player'].fresh_ap_into_hp_total}")
        ui.label(f"AP resets spent: {page_manager['active_player'].washes}")
        ui.label(f"AP resets cost: {page_manager['active_player'].washes * 3300}NX")
        ui.label("AP resets cost in time: %.2f years" % (page_manager['active_player'].washes * 3300 / (5000 * 365)))

@ui.refreshable
def gear_display(gears: List[Equipment]):
    for gear in gears:
        with ui.card().classes("border bg-red-100 gap-0"):
            ui.label(f"category: {gear.category}")
            ui.label(f"name: {gear.name}")
            ui.label(f"level requirement: {gear.level_req}")
            ui.label(f"INT: {gear.INT}")

@ui.refreshable
def da_thing_results(lvl, health_goal,base_int, washes, health, total_resets, is_seccesful, fresh_ap_into_hp, total_washes):
    if is_seccesful:
        color = 'bg-green-100'
    else:
        color = 'bg-red-100'
    with ui.element('div').classes(color):
        ui.label(f'For {health_goal} HP goal at lvl {lvl} with the registered gears')
        ui.label(f'The most optimal int is: {base_int}')
        ui.label(f'Fresh AP pent in MP: {washes}')
        ui.label(f'Fresh AP spent in HP: {fresh_ap_into_hp}')
        ui.label(f'HP after fully washing is: {health}')
        ui.label(f'Points reset from mana into other stats: {total_washes}')
        ui.label(f'Washing AP reset cost: {base_int - 4 + washes} (cost of resetting int back to 4 + fresh AP spent in MP)')
        ui.label(f'Total ap reset costs (including resetting the MP to HP): {total_resets}')
