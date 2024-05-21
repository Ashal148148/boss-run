from functools import partial
from typing import Annotated, Callable, Dict, List
from fastapi import Cookie, Request, Depends
from nicegui import app, ui
from nicegui.events import ValueChangeEventArguments
import nicegui
from ..identity import accept_user
from src.crud import equipment_crud, player_crud, ResourceNotFoundException
from sqlalchemy.orm import Session
from .dependencies import get_session
from ..schemas import PlayerSchema
from ..wash_calculator import Player, jobs, Equipment, do_the_stuff, mage_mp_wash_planner, mage_hp_wash_planner, battlecat_gears, reach_the_goal_no_matter_what

print('loading calculator for the first time')
with open('explanations.md', 'r') as f:
    explanations_md = f.read()

@ui.page('/')
def calculator(request: Request, session: Session = Depends(get_session)) -> None:
    user_id = accept_user(request, session)
    try: 
        player = PlayerSchema.model_validate(player_crud.read_by_user_id(session, user_id), from_attributes=True).model_dump()
        player['job'] = jobs[player['job']]
        player = Player(**player)
    except ResourceNotFoundException:
        player = Player(jobs['Archer/Thief'], 'AshalNL', 10, int_goal=350)
    gears_from_db = equipment_crud.read_by_session_id(session, user_id)
    page_manager: Dict[str, Player | str, List[Player]] = {'active_player': player, 'standby': []}
    int_gears: List[Equipment] = []
    for g, in gears_from_db:
        int_gears.append(Equipment(g.category, g.name, g.level_requirement, g.INT, g.id))
    page_manager["active_player"].gear_up(int_gears)
    ui.label("Welcome to BattleCat's HP washing calculator").classes("text-xl font-medium text-center w-full bg-slate-100 dark:bg-slate-800")
    ui.label("This calculator is an estimation, so take it with a grain of slat").classes('w-full text-center')
    with ui.card().classes('w-full'):
        ui.label("Terminology and Explanations").classes('text-lg font-medium')
        with ui.expansion('show'):
            ui.markdown(explanations_md) 
    with ui.card().classes('w-full'):
        ui.label('Registration').classes("text-lg font-medium")
        with ui.row():
            name = ui.input("name", placeholder='')
            ui.label("class: ").classes("text-lg")
            jobs_display = {1: "Archer/Thief" , 2: "Mage", 3: "Brawler", 4: "Gunslinger", 5: "Hero", 6: "Spearman/Paladin"}
            job = ui.select(jobs_display)
            ui.label("Maple warrior %")
            mw = ui.select({5:5, 10:10, 15:15})
            def on_click_lets_go(e):
                if name.value and mw.value is not None and jobs[jobs_display[job.value]]:
                    page_manager["active_player"]=Player(jobs[jobs_display[job.value]], name.value, mw.value)
                    player_crud.save(session=session ,user_id=user_id, player=page_manager["active_player"])
                    print(page_manager['active_player'])
                    player_card.refresh()
                    strategy_card.refresh()
                    wash_planner_card.refresh()
                    ui.notify("successfully registered")
                else:
                    ui.notify("please make sure to fill all fields")
            ui.button("let's go", on_click=on_click_lets_go) 
        gears_carousel(int_gears, session)
        gears_registration(int_gears, session, request)
    
    wash_planner_card(page_manager, int_gears)
    
    with ui.card().classes('w-full'):
        ui.label('The calculator').classes('text-lg font-medium')
        with ui.row().classes('flex-nowrap'):
            player_card(page_manager, int_gears, session, user_id)
            with ui.column().classes("flex-nowrap"):
                strategy_card(page_manager)
                with ui.row():
                    with ui.card().classes('bg-blue-200'):
                        ui.label('Levels').classes('text-lg font-medium')
                        with ui.row():
                            def one_level_up():
                                page_manager["active_player"].progress(1, int_gears)
                                player_card.refresh()
                            ui.button("1 Up", on_click=one_level_up)
                            def ten_level_up():
                                page_manager["active_player"].progress(10, int_gears)
                                player_card.refresh()
                            ui.button("10 Up", on_click=ten_level_up)
                            levels = ui.number('levels:', value=1, max=199, min=1)
                            def custom_level_up():
                                page_manager["active_player"].progress(int(levels.value), int_gears)
                                player_card.refresh()
                            ui.button("Level Up", on_click=custom_level_up)
                with ui.row():
                    with ui.card().classes('bg-yellow-200'):
                        ui.label('Washing').classes('text-lg font-medium')
                        with ui.row():                            
                            def one_mana_wash():
                                page_manager["active_player"].mp_wash(1)
                                player_card.refresh()
                            ui.button('1 Mana wash', on_click=one_mana_wash).tooltip('add fresh AP into MP, Remove the same amount of AP from MP and add it to the main stat')
                            def ten_mana_wash():
                                page_manager["active_player"].mp_wash(10)
                                player_card.refresh()
                            ui.button('10 Mana washes', on_click=ten_mana_wash).tooltip('add fresh AP into MP, Remove the same amount of AP from MP and add it to the main stat')
                            custom_mana_washes = ui.number('washes', value=1, min=1)
                            def mana_wash():
                                page_manager["active_player"].mp_wash(int(custom_mana_washes.value))
                                player_card.refresh()
                            ui.button('Mana wash', on_click=mana_wash).tooltip('add fresh AP into MP, Remove the same amount of AP from MP and add it to the main stat')
                        with ui.row():
                            def one_hp_wash():
                                page_manager["active_player"].hp_wash(1)
                                player_card.refresh()
                            ui.button('1 HP wash', on_click=one_hp_wash).tooltip('Reset points from MP into HP')
                            def ten_hp_wash():
                                page_manager["active_player"].hp_wash(10)
                                player_card.refresh()
                            ui.button('10 HP washes', on_click=ten_hp_wash).tooltip('Reset points from MP into HP')
                            custom_hp_washes = ui.number('washes', value=1, min=1)
                            def hp_wash():
                                page_manager["active_player"].hp_wash(int(custom_hp_washes.value))
                                player_card.refresh()
                            ui.button('HP wash', on_click=hp_wash).tooltip('Reset points from MP into HP')
                        with ui.row():
                            def full_hp_wash():
                                page_manager["active_player"].hp_wash()
                                player_card.refresh()
                            ui.button('Reset all bonus mp into hp', on_click=full_hp_wash).classes('red')
                            def reset_INT():
                                page_manager["active_player"].fix_char()
                                player_card.refresh()
                                strategy_card.refresh()
                            ui.button('Reset INT', on_click=reset_INT).classes('red')

    ui.label("found a bug? contact me via discord: shaul_carvalho")
    # ui.label("donations would be appreciated <todo>")
            

@ui.refreshable
def wash_planner_card(page_manager: Dict[str, Player], int_gears: List[Equipment]):
    with ui.card().classes('w-full'):
        ui.label('HP wash planner').classes('text-lg font-medium')
        ui.label('This feature will use the class, gears and Maple Warrior % you entered and calculate the cheapest way to reach your HP goal by your lvl goal')
        if page_manager['active_player'].job.name != 'Mage':
            ui.label('The result will tell you what Base INT you should use and how many points to MP wash, how many points to add to HP and how much everything will cost')
            ui.label('The calculation will take into account resetting your base INT to 4 once you hit your lvl goal')
            ui.label('NX focused wash')
            with ui.row():
                hp_goal = ui.number('HP goal')
                lvl_goal = ui.number('level goal')
                def on_calculate_click():
                    base_int, washes, health, total_resets, success, fresh_ap_into_hp, total_washes = do_the_stuff(page_manager['active_player'], int_gears, int(lvl_goal.value), int(hp_goal.value))
                    da_thing_results(int(lvl_goal.value), int(hp_goal.value), base_int, washes, health, total_resets, success, fresh_ap_into_hp, total_washes)
                    da_thing_results.refresh()
                ui.button('do the thing', on_click=on_calculate_click)
            ui.label('Level focused wash')
            with ui.row():
                hp_goal2 = ui.number('HP goal')
                lvl_goal2 = ui.number('level goal')
                def on_calculate_hp_wash_click():
                    base_int, washes, health, total_resets, success, fresh_ap_into_hp, total_washes, mp_wash_starting_int = reach_the_goal_no_matter_what(page_manager['active_player'], int_gears, int(lvl_goal2.value), int(hp_goal2.value))
                    da_thing_results(int(lvl_goal2.value), int(hp_goal2.value), base_int, washes, health, total_resets, success, fresh_ap_into_hp, total_washes, mp_wash_starting_int)
                    da_thing_results.refresh()
                ui.button('do the thing', on_click=on_calculate_hp_wash_click)
        else:
            ui.label('Mage MP wash planner')
            with ui.row():
                mp_goal = ui.number('MP goal')
                mage_mp_lvl_goal = ui.number('level goal')
                def on_calculate_mp_click():
                    start_level, total_washes, total_mp, is_successful = mage_mp_wash_planner(page_manager['active_player'], int_gears, int(mage_mp_lvl_goal.value), int(mp_goal.value))
                    mage_wash_planner_results(start_level, total_washes, 0, total_mp, is_successful)
                    # mage_wash_planner_results.refresh()
                ui.button('do the thing', on_click=on_calculate_mp_click)
            ui.label('Mage HP wash planner')
            with ui.row():
                mage_hp_goal = ui.number('HP goal')
                mage_mp_goal = ui.number('MP goal')
                mage_hp_lvl_goal = ui.number('level goal')
                def on_calculate_mage_hp_click():
                    start_level, total_washes, total_hp, total_mp, is_successful = mage_hp_wash_planner(page_manager['active_player'], int_gears, int(mage_hp_lvl_goal.value), int(mage_hp_goal.value), int(mage_mp_goal.value))
                    mage_wash_planner_results(start_level, total_washes, total_hp, total_mp, is_successful)
                    # mage_wash_planner_results.refresh()
                ui.button('do the thing', on_click=on_calculate_mage_hp_click)


@ui.refreshable
def gears_registration(int_gears: List[Equipment], session: Session, request: Request):
    with ui.expansion('Gears registration').classes('bg-blue-300' if len(int_gears) > 0 else 'bg-red-300'):
        ui.label("please register the int gears you plan on using")
        eq_category = ui.select(options=Equipment.categories, with_input=True).classes('w-40')
        eq_name = ui.input('name')
        eq_lvl_req = ui.number('level requirement')
        eq_INT = ui.number('INT')        

        def add_gear():
            if eq_category.value and eq_name.value and eq_lvl_req.value and eq_INT.value:
                new_gear = equipment_crud.create(session, request.session["id"], eq_category.value, eq_name.value, int(eq_lvl_req.value), int(eq_INT.value))
                int_gears.append(Equipment(eq_category.value, eq_name.value, int(eq_lvl_req.value), int(eq_INT.value), new_gear.id))                    
                if len(int_gears) == 1:  # the fist gear was added so we change color
                    gears_registration.refresh()
                gears_carousel.refresh()
                ui.notify("gear added")
            else:
                ui.notify("please make sure to fill all fields")

        def battlecat_gears_and_refresh():
            battlecat_gears(int_gears)
            gears_registration.refresh()
            gears_carousel.refresh() 

        ui.button("gears", on_click=battlecat_gears_and_refresh).tooltip('this button will add all my (BattleCats) gears until you refresh the page')
        ui.button("add gear", on_click=add_gear) 


@ui.refreshable
def gears_carousel(int_gears: List[Equipment], session: Session):
    gear_tabs = []
    with ui.tabs().classes('w-half') as tabs:
        for gear in reversed(int_gears):  # reverse so that the latest addition appears first
            gear_tabs.append(ui.tab(gear.name))
    if gear_tabs:
        with ui.tab_panels(tabs, value=gear_tabs[0]):
            for t, gear in zip(gear_tabs, reversed(int_gears)):             
                def on_click_remove(int_gearz, gearz):
                    int_gearz.remove(gearz)
                    equipment_crud.delete(session, gearz.id)
                    if len(int_gearz) == 0:  # we removed the last gear so change color
                        gears_registration.refresh()
                    gears_carousel.refresh()
                    ui.notify("gear removed")                    
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
    with ui.dialog() as dialog, ui.card():
        gear_display(page_manager["active_player"].equipment)
        ui.button('close', on_click=dialog.close)
    def on_show_gear():
        gear_display.refresh()
        dialog.open()
    with ui.element('div').classes('p-2 bg-blue-100'):
        ui.label(page_manager['active_player'].name)
        ui.label(f"level: {page_manager['active_player'].level}")
        ui.label(f"job: {page_manager['active_player'].job.name}")
        ui.label(f"Base INT goal: {page_manager['active_player'].int_goal}")
        ui.label(f"Base INT: {page_manager['active_player'].INT}")
        ui.label(f"Gears bonus INT: {page_manager['active_player'].gears_int}").on('click',handler=on_show_gear).classes('text-blue cursor-pointer').tooltip('Click to view equipped gear')
        ui.label(f"Total INT: {page_manager['active_player'].total_int}")        
        ui.label(f"Bonus mana: {page_manager['active_player'].bonus_mana}")
        ui.label(f"Total mana: {page_manager['active_player'].mana}")
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
        ui.button("Save").tooltip('coming soon...')
        def reset_character():
            page_manager['active_player'].reset_player()
            player_card.refresh()
        ui.button("Reset", on_click=reset_character).tooltip("Reset back to lvl 1")

@ui.refreshable
def gear_display(gears: List[Equipment]):
    for gear in gears:
        with ui.card().classes("border bg-red-100 gap-0"):
            ui.label(f"category: {gear.category}")
            ui.label(f"name: {gear.name}")
            ui.label(f"level requirement: {gear.level_req}")
            ui.label(f"INT: {gear.INT}")

@ui.refreshable
def da_thing_results(lvl, health_goal,base_int, washes, health, total_resets, is_successful, fresh_ap_into_hp, total_washes, mp_wash_starting_int = 0):
    if is_successful:
        color = 'bg-green-100'
    else:
        color = 'bg-red-100'
    with ui.element('div').classes(color):
        ui.label(f'For {health_goal} HP goal at lvl {lvl} with the registered gears')
        ui.label(f'The most optimal int is: {base_int}')
        if mp_wash_starting_int:
            ui.label(f'Start MP washing at {mp_wash_starting_int} base int')
        ui.label(f'Fresh AP spent in MP: {washes}')
        ui.label(f'Fresh AP spent in HP: {fresh_ap_into_hp}')
        ui.label(f'HP after fully washing is: {health}')
        ui.label(f'Points reset from mana into other stats: {total_washes}')
        ui.label(f'Washing AP reset cost: {base_int - 4 + washes} (cost of resetting int back to 4 + fresh AP spent in MP/HP)')
        ui.label(f'Total ap reset costs (including resetting the MP to HP): {total_resets}')


@ui.refreshable
def mage_wash_planner_results(start_level, total_washes, total_hp, total_mp, is_successful):
    if is_successful:
        color = 'bg-green-100'
    else:
        color = 'bg-red-100'
    with ui.element('div').classes(color):
        ui.label(f'To reach your goals at your goal level you need to start washing at level: {start_level}')
        ui.label(f'Reset scrolls needed: {total_washes}')        
        ui.label(f'MP after fully washing is: {total_mp}')
        if total_hp:
            ui.label(f'HP after fully washing is: {total_hp}')

@ui.refreshable
def strategy_card(page_manager: Dict[str, Player]):
    with ui.row():
        with ui.card().classes('bg-purple-200'):
            ui.label('Strategy').classes('text-lg font-medium')
            with ui.row():                            
                def on_toggle_add_int():
                    page_manager["active_player"].is_adding_int = not page_manager["active_player"].is_adding_int
                ui.checkbox('Add INT', value=page_manager["active_player"].is_adding_int, on_change=on_toggle_add_int).tooltip("while base INT is under the Base INT Goal upon level up add 5 points into INT (stale or fresh, whatever is available)")
                def on_base_int_goal_change(change_event: ValueChangeEventArguments):
                    page_manager['active_player'].int_goal = int(change_event.value)
                    player_card.refresh()
                ui.number("Base INT goal", value=page_manager['active_player'].int_goal, on_change=on_base_int_goal_change)
                def on_toggle_fresh_ap_into_hp():
                    page_manager["active_player"].is_adding_fresh_ap_into_hp = not page_manager["active_player"].is_adding_fresh_ap_into_hp
                    player_card.refresh()
                ui.checkbox('Add fresh AP into HP', value=page_manager["active_player"].is_adding_fresh_ap_into_hp, on_change=on_toggle_fresh_ap_into_hp).tooltip('If your class has an HP growth skill (warriors/brawlers) HP washing while this box is checked box will make your character spend fresh AP on HP, turning the fresh AP into stale AP')
                def on_toggle_mp_wash_before_int():
                    page_manager["active_player"].is_mp_wash_before_int = not page_manager["active_player"].is_mp_wash_before_int
                    player_card.refresh()
                ui.checkbox('MP Wash before adding int', value=page_manager["active_player"].is_mp_wash_before_int, on_change=on_toggle_mp_wash_before_int).tooltip('Each level put all fresh AP into MP')
