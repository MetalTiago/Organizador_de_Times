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
from localization import get_string

def main(page: ft.Page):
    # Título inicial (será atualizado após carregar o estado)
    page.title = "Organizador de Times" 
    page.window_height = 840
    page.window_width = 400
    page.padding = 10
    
    # Define os temas claro e escuro
    page.theme = ft.Theme(color_scheme_seed="blue", font_family="Roboto")
    dark_theme_obj = ft.Theme(color_scheme_seed="blue", font_family="Roboto")
    dark_theme_obj.brightness = ft.Brightness.DARK
    page.dark_theme = dark_theme_obj

    # Cria o estado (que carrega as preferências salvas)
    execute_migrations()
    app_state = AppState(page)
    set_page_ref(app_state) # Passa a referência do estado para os componentes

    # --- DEFINE O TEMA INICIAL E O TÍTULO COM BASE NAS PREFERÊNCIAS CARREGADAS ---
    page.theme_mode = app_state.preferred_theme_mode if app_state.preferred_theme_mode else "dark" # Usa o salvo ou padrão dark
    page.title = get_string(app_state, "app_title") 

    app_state.input_container = build_input_container(app_state)
    app_state.edit_container = build_edit_container(app_state)

    # Define o ícone inicial do botão de tema com base no tema carregado/definido
    initial_icon = ft.icons.WB_SUNNY if page.theme_mode == "light" else ft.icons.NIGHTS_STAY
    app_state.theme_toggle_button = ft.IconButton(
        icon=initial_icon, 
        tooltip=get_string(app_state, "toggle_theme_tooltip")
    )
    
    # --- ATUALIZA A FUNÇÃO toggle_theme PARA SALVAR A PREFERÊNCIA ---
    def toggle_theme(e):
        # Alterna o tema
        new_theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.theme_mode = new_theme_mode
        # Atualiza o ícone e tooltip do botão
        app_state.theme_toggle_button.icon = ft.icons.WB_SUNNY if new_theme_mode == "light" else ft.icons.NIGHTS_STAY
        app_state.theme_toggle_button.tooltip = get_string(app_state, "toggle_theme_tooltip")
        # --- SALVA A NOVA PREFERÊNCIA ---
        app_state.save_theme_preference(new_theme_mode) 
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

    def navigate_to(view_name):
        page.clean()
        page.route = f"/{view_name}"
        builder = view_builders.get(view_name)
        if not builder:
            page.add(ft.Text(f"Erro: View '{view_name}' não encontrada."))
            return

        view_to_display = builder(app_state)
        page.add(view_to_display)
        
        # Lógica de inicialização das views (sem alterações aqui)
        if view_name == "main":
            if hasattr(app_state, 'populate_lists_dropdown') and app_state.populate_lists_dropdown:
                app_state.populate_lists_dropdown()
            atualizar_tabela(app_state)
        elif view_name == "selection":
            if hasattr(app_state, 'montar_lista_jogadores') and app_state.montar_lista_jogadores:
                app_state.montar_lista_jogadores()
        elif view_name == "results":
             if not app_state.team_count_slider.value or len(app_state.selecionados) < int(app_state.team_count_slider.value):
                # Mensagem de erro deveria usar get_string também
                page.snack_bar = ft.SnackBar(ft.Text("Verifique o número de times e jogadores."), bgcolor=ft.colors.RED_700); page.snack_bar.open = True 
                navigate_to("selection")
                return
             else:
                if hasattr(app_state, 'reorganize_teams') and app_state.reorganize_teams:
                    page.run_task(app_state.reorganize_teams)
        
        page.update()
    app_state.navigate_to = navigate_to
    
    navigate_to("main")

ft.app(target=main, assets_dir="assets")