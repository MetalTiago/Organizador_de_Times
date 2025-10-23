# main.py
import flet as ft
# Usa ft.colors.
# import asyncio
from db_handler import execute_migrations
from app_state import AppState
from views.main_view import build_main_view
from views.selection_view import build_selection_view
from views.results_view import build_results_view
from views.manage_players_view import build_manage_players_view
from views.settings_view import build_settings_view
from views.privacy_policy_view import build_privacy_policy_view
from views.terms_of_use_view import build_terms_of_use_view
from components import set_page_ref, build_input_container, build_edit_container, atualizar_tabela
from localization import get_string
# REMOVIDO: import ads_manager

# Importa funções de contagem se necessário (aqui ou onde for usado)
try:
    from db_handler import count_all_players, count_custom_lists # Importa counts
    PLAYER_LIMIT_FREE = 20 # Define limite aqui também se usado em show_form
    LIST_LIMIT_FREE = 2 # Define limite aqui também se usado em show_form (ou melhor importar da view)
except ImportError:
    def count_all_players(): return 0
    def count_custom_lists(): return 0
    PLAYER_LIMIT_FREE = 20
    LIST_LIMIT_FREE = 2


def main(page: ft.Page):
    page.title = "Organizador de Times"
    page.window.height = 840
    page.window.width = 400
    page.padding = 10

    page.theme = ft.Theme(color_scheme_seed="blue", font_family="Roboto")
    dark_theme_obj = ft.Theme(color_scheme_seed="blue", font_family="Roboto")
    dark_theme_obj.brightness = ft.Brightness.DARK
    page.dark_theme = dark_theme_obj

    execute_migrations()
    app_state = AppState(page)
    set_page_ref(app_state) # Passa a referência do estado para os componentes

    page.theme_mode = app_state.preferred_theme_mode
    page.title = get_string(app_state, "app_title")

    # REMOVIDO: Inicialização de anúncios
    # if not app_state.is_pro: ads_manager.initialize_ads(page)

    app_state.input_container = build_input_container(app_state)
    app_state.edit_container = build_edit_container(app_state)

    initial_icon_name = "wb_sunny" if page.theme_mode == "light" else "nights_stay"
    app_state.theme_toggle_button = ft.IconButton(
        icon=initial_icon_name,
        tooltip=get_string(app_state, "toggle_theme_tooltip")
    )

    def toggle_theme(e):
        new_theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.theme_mode = new_theme_mode
        app_state.theme_toggle_button.icon = "wb_sunny" if new_theme_mode == "light" else "nights_stay"
        app_state.theme_toggle_button.tooltip = get_string(app_state, "toggle_theme_tooltip")
        app_state.save_theme_preference(new_theme_mode)
        page.update()
    app_state.theme_toggle_button.on_click = toggle_theme

    view_builders = {
        "main": build_main_view,
        "selection": build_selection_view,
        "results": build_results_view,
        "manage_players": build_manage_players_view,
        "settings": build_settings_view,
        "privacy_policy": build_privacy_policy_view,
        "terms_of_use": build_terms_of_use_view,
    }

    def show_form():
        # A verificação de limite está agora em components.py (build_input_container > save_user)
        # Não precisamos duplicar aqui, apenas garantir que components.py tem acesso a count_all_players
        if app_state.populate_new_player_lists_form:
            app_state.populate_new_player_lists_form()
        app_state.input_container.visible = True
        app_state.main_view_content.visible = False
        app_state.update()

    def hide_form():
        # REMOVIDO: Chamada de anúncio intersticial
        # if not app_state.is_pro: ads_manager.show_interstitial(page)
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
            # TODO: Adicionar string de erro
            page.add(ft.Text(f"Erro: View '{view_name}' não encontrada."))
            return

        view_to_display = builder(app_state)

        # --- Lógica de Banner Removida ---
        # Adiciona apenas a view principal diretamente à página
        page.add(view_to_display)

        # Lógica de inicialização específica de cada view
        if view_name == "main":
            if hasattr(app_state, 'populate_lists_dropdown') and app_state.populate_lists_dropdown: app_state.populate_lists_dropdown()
            atualizar_tabela(app_state)
        elif view_name == "selection":
             if hasattr(app_state, 'team_count_slider') and app_state.team_count_slider: app_state.team_count_text.value = get_string(app_state, "teams_count", count=int(app_state.team_count_slider.value))
             if hasattr(app_state, 'montar_lista_jogadores') and app_state.montar_lista_jogadores: app_state.montar_lista_jogadores()
        elif view_name == "results":
             if not app_state.team_count_slider or not app_state.team_count_slider.value or len(app_state.selecionados) < int(app_state.team_count_slider.value):
                # TODO: Traduzir
                page.snack_bar = ft.SnackBar(ft.Text("Verifique o número de times e jogadores selecionados."), bgcolor=ft.colors.RED_700); page.snack_bar.open = True # Usa ft.colors.
                page.clean(); navigate_to("selection"); return
             # else: A organização inicial é chamada DENTRO de build_results_view

        page.update() # Atualiza a página após adicionar a nova view
    app_state.navigate_to = navigate_to

    navigate_to("main")

ft.app(target=main, assets_dir="assets")