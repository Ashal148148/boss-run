from typing import Annotated, Dict, List
from fastapi import Cookie, Request, Depends
from nicegui import app, ui
from src.crud import user_crud
from sqlalchemy.orm import Session
from .dependencies import get_session
from ..wash_calculator import Player, jobs, Equipment

@ui.page('/')
def calculator(request: Request, session: Session = Depends(get_session)) -> None:
    page_manager: Dict[str, Player | str, List[Player]] = {'active_player': Player(350, jobs['thief'], 'AshalNL', 10), 'standby': []}
    int_gears: List[Equipment] = []
    ui.label("Welcome to BattleCat's HP washing calculator")
    ui.label("Before we begin ill need some info from you")
    with ui.tabs().classes('w-full') as tabs:
        tab_one = ui.tab('gears')
        tab_two = ui.tab('class')
    with ui.tab_panels(tabs, value=tab_one).classes('w-full'):
        with ui.tab_panel(tab_one):
            eq_category = ui.input('category')
            eq_name = ui.input('name')
            eq_lvl_req = ui.number('level requirement')
            eq_INT = ui.number('INT')

            def fun():
                int_gears.append( Equipment("hat",'horns',22, 5))
                int_gears.append( Equipment("hat",'zak',50, 32))
                int_gears.append( Equipment("ear", 'ear',15, 8))
                int_gears.append( Equipment("wand", 'wooden',10, 8))
                int_gears.append(Equipment("overall", 'bathrobe',20, 20))
                int_gears.append( Equipment("pendant", 'yellow muffler',30, 3))
                int_gears.append( Equipment("pendant", 'dep star',50, 5))
                int_gears.append( Equipment("pendant", 'htp',120, 22))
                int_gears.append( Equipment("shield", 'pan shield',10,7))
                int_gears.append( Equipment("eye", 'raccun',45, 11))
                int_gears.append(Equipment("cape", 'ragged cape', 32, 9))
                int_gears.append(Equipment("cape", 'yellow cape', 50, 12))
                int_gears.append(Equipment("cape", 'cwkpq cape',80, 18))
                int_gears.append(Equipment("shoe", 'slime shoe',30, 1))
                int_gears.append(Equipment("glove", 'red markers', 20, 11))
                gears_carousel.refresh()

            def add_gear():
                if eq_category.value and eq_name.value and eq_lvl_req.value and eq_INT.value:
                    int_gears.append(Equipment(eq_category.value, eq_name.value, eq_lvl_req.value, eq_INT.value))
                    gears_carousel.refresh()
                else:
                    ui.notify("please make sure to fill all fields")
            ui.button("gears", on_click=fun)
            ui.button("add gear", on_click=add_gear)
            gears_carousel(int_gears)
            
        with ui.tab_panel(tab_two):
            ui.label("please register the int gears you plan on using")
            name = ui.input("name", placeholder='')
            INT_goal = ui.number(label='Base INT goal')
            ui.label("class: ")
            jobs_display = {1: "thief" , 2: "archer", 3: "bucc", 4: "sair", 5: "hero_pala", 6: "dk"}
            job = ui.select(jobs_display)
            mw = ui.number(label="Maple warrior %")
            def on_click_lets_go(e):
                if INT_goal.value and jobs[jobs_display[job.value]] and name.value and mw.value:
                    page_manager["active_player"]=Player(INT_goal.value, jobs[jobs_display[job.value]], name.value, mw.value)
                    print(page_manager['active_player'])
                    player_card.refresh()
                else:
                    ui.notify("please make sure to fill all fields")
            ui.button("let's go", on_click=on_click_lets_go)   
    with ui.row():
        levels = ui.number('levels:', value=1, max=199, min=1)
        def level_up():
            page_manager["active_player"].progress(int(levels.value), False, int_gears)
            player_card.refresh()
        ui.button("Level Up", on_click=level_up)
        def on_toaggle_add_int():
            page_manager["active_player"].is_adding_int = not page_manager["active_player"].is_adding_int
            print(page_manager["active_player"])
        ui.checkbox('Add INT', value=page_manager["active_player"].is_adding_int, on_change=on_toaggle_add_int)
        mana_washes = ui.number('washes', value=1, min=1)
        def mana_wash():
            page_manager["active_player"].mp_wash(int(mana_washes.value))
            player_card.refresh()
        ui.button('Mana wash', on_click=mana_wash)
        hp_washes = ui.number('washes', value=1, min=1)
        def hp_wash():
            page_manager["active_player"].hp_wash(int(hp_washes))
            player_card.refresh()
        ui.button('HP wash', on_click=hp_wash)
        def full_hp_wash():
            page_manager["active_player"].hp_wash()
            player_card.refresh()
        ui.button('Full HP wash', on_click=full_hp_wash)
        def reset_INT():
            page_manager["active_player"].fix_char()
            player_card.refresh()
        ui.button('Reset INT', on_click=reset_INT)
        with ui.dialog().classes("w-full") as dialog, ui.card().classes("w-full"):
            gear_display(page_manager["active_player"].equipment)
            ui.button('close', on_click=dialog.close)
        def on_show_gear():
            gear_display.refresh()
            dialog.open()
        ui.button('Show equiped gear', on_click=on_show_gear)
        player_card(page_manager, int_gears)
            


@ui.refreshable
def gears_carousel(int_gears: List[Equipment]):
    gear_tabs = []
    with ui.tabs().classes('w-half') as tabs:
        for gear in int_gears:
            gear_tabs.append(ui.tab(gear.name))
    if gear_tabs:
        with ui.tab_panels(tabs, value=gear_tabs[0]).classes(''):
            for t, gear in zip(gear_tabs, int_gears): 
                with ui.tab_panel(t):
                    ui.label(f"category: {gear.category}")
                    ui.label(f"name: {gear.name}")
                    ui.label(f"level requirement: {gear.level_req}")
                    ui.label(f"INT: {gear.INT}")


@ui.refreshable
def player_card(page_manager: Dict[str, Player], int_gears: List[Equipment]):
    with ui.element('div').classes('p-2 bg-blue-100'):
        ui.label('inside a colored div')
        ui.label(page_manager['active_player'].name)
        ui.label(f"level: {page_manager['active_player'].level}")
        ui.label(f"job: {page_manager['active_player'].job}")
        ui.label(f"Base INT: {page_manager['active_player'].INT}")
        ui.label(f"Total INT: {page_manager['active_player'].total_int}")
        ui.label(f"Bonus mana: {page_manager['active_player'].bonus_mana}")
        ui.label(f"Bonus health: {page_manager['active_player'].bonus_HP}")
        ui.label(f"Total health: {page_manager['active_player'].health}")
        ui.label(f"Fresh AP: {page_manager['active_player'].fresh_AP}")
        ui.label(f"Stale AP: {page_manager['active_player'].stale_ap}")
        ui.label(f"Main stat: {page_manager['active_player'].main_stat}")
        ui.label(f"AP resets spent: {page_manager['active_player'].washes}")
        ui.label(f"AP resets cost: {page_manager['active_player'].washes * 3300}NX")
        ui.label("AP resets cost in time: %.2f years" % (page_manager['active_player'].washes * 3300 / (5000 * 365)))

@ui.refreshable
def gear_display(gears: List[Equipment]):
    for gear in gears:
        with ui.card().classes("border bg-red-100"):
            # ui.label(f"category: {gear.category}")
            ui.label(f"name: {gear.name}")
            # ui.label(f"level requirement: {gear.level_req}")
            ui.label(f"INT: {gear.INT}")