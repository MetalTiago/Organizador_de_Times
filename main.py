# main.py
import flet as ft
from db_handler import execute_migrations
from app_state import AppState
from views.main_view import build_main_view
from views.selection_view import build_selection_view
from views.results_view import build_results_view
from views.manage_players_view import build_manage_players_view
from views.settings_view import build_settings_view
from components import set_page_ref, build_input_container, build_edit_container, atualizar_tabela

def main(page: ft.Page):
    page.title = "Organizador de Times"
    page.window_height = 840
    page.window_width = 400
    page.padding = 10
    
    page.theme = ft.Theme(color_scheme_seed="blue", font_family="Roboto")
    dark_theme_obj = ft.Theme(color_scheme_seed="blue", font_family="Roboto")
    dark_theme_obj.brightness = ft.Brightness.DARK
    page.dark_theme = dark_theme_obj
    page.theme_mode = "dark"

    execute_migrations()
    app_state = AppState(page)
    set_page_ref(app_state) 

    app_state.input_container = build_input_container(app_state)
    app_state.edit_container = build_edit_container(app_state)

    app_state.theme_toggle_button = ft.IconButton(icon=ft.icons.NIGHTS_STAY, tooltip="Alternar Tema")
    def toggle_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        app_state.theme_toggle_button.icon = ft.icons.WB_SUNNY if page.theme_mode == "light" else ft.icons.NIGHTS_STAY
        page.update()
    app_state.theme_toggle_button.on_click = toggle_theme

    view_builders = {
        "main": build_main_view,
        "selection": build_selection_view,
        "results": build_results_view,
        "manage_players": build_manage_players_view,
        "settings": build_settings_view
    }

    def show_form():
        if app_state.populate_new_player_lists_form:
            app_state.populate_new_player_lists_form()
        app_state.input_container.visible = True
        app_state.main_view_content.visible = False
        app_state.update()

    def hide_form():
        app_state.input_container.visible = False
        app_state.main_view_content.visible = True
        app_state.update() 
    
    app_state.show_form = show_form
    app_state.hide_form = hide_form 

    # --- NAVEGAÇÃO COM A ORDEM CORRETA ---
    def navigate_to(view_name):
        page.clean()
        page.route = f"/{view_name}"
        builder = view_builders.get(view_name)
        if not builder:
            page.add(ft.Text(f"Erro: View '{view_name}' não encontrada."))
            return

        # 1. Constrói a view
        view_to_display = builder(app_state)
        # 2. Adiciona à página
        page.add(view_to_display)
        
        # 3. Executa a lógica de inicialização DEPOIS de a view estar na página
        if view_name == "main":
            # A função para popular o dropdown agora está no app_state
            if hasattr(app_state, 'populate_lists_dropdown') and app_state.populate_lists_dropdown:
                app_state.populate_lists_dropdown()
            # A função para atualizar a tabela continua sendo chamada
            atualizar_tabela(app_state)
        elif view_name == "selection":
            # A mesma lógica se aplica aqui para garantir que funcione
            if hasattr(app_state, 'montar_lista_jogadores') and app_state.montar_lista_jogadores:
                app_state.montar_lista_jogadores()
        elif view_name == "results":
             if not app_state.team_count_slider.value or len(app_state.selecionados) < int(app_state.team_count_slider.value):
                page.snack_bar = ft.SnackBar(ft.Text("Verifique o número de times e jogadores."), bgcolor=ft.colors.RED_700); page.snack_bar.open = True
                navigate_to("selection")
                return
             else:
                if hasattr(app_state, 'reorganize_teams') and app_state.reorganize_teams:
                    page.run_task(app_state.reorganize_teams)
        
        page.update()
    app_state.navigate_to = navigate_to
    
    # Inicia o aplicativo
    navigate_to("main")

ft.app(target=main, assets_dir="assets")   