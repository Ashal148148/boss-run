from nicegui import ui, app
from fastapi.responses import RedirectResponse


@ui.page('/login')
def login_page() -> None:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if 'hi' == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.open('/')
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)