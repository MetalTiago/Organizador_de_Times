# views/selection_view.py
import flet as ft
from db_handler import get_players_by_list
import base64
import os
from localization import get_string
from components import apply_opacity # Importa helper
# Importa o typing para o AppState (evita erro de lint)
try:
    from app_state import AppState
except ImportError:
    pass

APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".organizador_de_times")

def build_selection_view(state: 'AppState'):

    def update_selected_count():
         """Atualiza o texto que mostra o número de jogadores selecionados."""
         if state and hasattr(state, 'selected_count_text'):
             state.selected_count_text.value = get_string(state, "selected_players_count", count=len(state.selecionados))

    # --- CORREÇÃO (API 0.28.3) ---
    # Revertendo para a lógica original do seu 'selection_view.py'
    # que usa a 'indicator_strip'
    def toggle_selection(jogador, indicator, container, name_text):
        """Adiciona ou remove um jogador da lista de selecionados."""
        is_selected = any(s[0] == jogador[0] for s in state.selecionados)
        
        if is_selected:
            # Remove
            state.selecionados[:] = [s for s in state.selecionados if s[0] != jogador[0]]
            indicator.visible = False
            container.bgcolor = None
            name_text.color = None
        else:
            # Adiciona
            state.selecionados.append(jogador)
            # --- CORRIGIDO (Sintaxe 0.28 - Cores como Strings) ---
            indicator.visible = True
            container.bgcolor = apply_opacity("primary", 0.05) 
            name_text.color = "primary"
            # --- FIM DA CORREÇÃO ---
            
        update_selected_count()
        state.update()
    # --- FIM DA CORREÇÃO ---

    def montar_lista_jogadores():
        """Constrói a lista de jogadores da lista ativa."""
        state.checkbox_list.controls.clear()
        users = get_players_by_list(state.active_list_id)
        
        for jogador in users:
            is_selected = any(s[0] == jogador[0] for s in state.selecionados)
            
            # --- CORRIGIDO (API 0.28.3) ---
            avatar_display = ft.Container(
                width=44, height=44, 
                content=ft.Icon(name="person_outline"), # API 0.28.3: String
                border_radius=22, 
                bgcolor=apply_opacity("on_surface", 0.1)
            ) 
            # --- FIM DA CORREÇÃO ---
            
            player_id, photo_path = jogador[0], jogador[3]
            if photo_path:
                image_base64 = state.photo_cache.get(player_id)
                if not image_base64:
                    try:
                        full_path = os.path.join(APP_DATA_DIR, photo_path)
                        if os.path.exists(full_path):
                            with open(full_path, "rb") as f: 
                                image_base64 = base64.b64encode(f.read()).decode('utf-8')
                                state.photo_cache[player_id] = image_base64 # Armazena no cache
                    except Exception as img_err: 
                        image_base64 = None
                        print(f"Erro img selection: {img_err}")
                
                if image_base64: 
                    avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=22)

            # --- CORREÇÃO (API 0.28.3) ---
            # Revertendo para a lógica original da 'indicator_strip'
            indicator_strip = ft.Container(
                width=5, height=55, 
                bgcolor="primary", # Cor como string
                border_radius=4, 
                visible=is_selected
            ) 
            player_name_text = ft.Text(jogador[1], color="primary" if is_selected else None) 
            list_tile = ft.ListTile(title=player_name_text, leading=avatar_display)
            
            content_container = ft.Container(
                content=list_tile, 
                bgcolor=apply_opacity("primary", 0.05) if is_selected else None, 
                border=ft.border.only(bottom=ft.BorderSide(1, apply_opacity("on_surface", 0.1))), 
                border_radius=8, 
                expand=True
            ) 
            # --- FIM DA CORREÇÃO ---
            
            # Define o lambda para o clique
            list_tile.on_click = lambda e, j=jogador, i=indicator_strip, c=content_container, nt=player_name_text: toggle_selection(j, i, c, nt)
            
            state.checkbox_list.controls.append(
                ft.Row(
                    [indicator_strip, content_container], 
                    spacing=5, 
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        update_selected_count()
        
    state.montar_lista_jogadores = montar_lista_jogadores

    def clear_selection(e): 
        """Limpa a seleção e reconstrói a lista."""
        state.selecionados.clear()
        montar_lista_jogadores()
        state.update()

    def update_team_count_text_and_save(e):
        """Atualiza o texto do slider e salva a preferência."""
        count = int(e.control.value)
        state.team_count_text.value = get_string(state, "teams_count", count=count)
        state.save_last_team_count_preference(count) 
        state.update() 

    # --- Lógica de Limite REMOVIDA (Fase 1.5) ---
    max_teams_allowed = 10
    divisions_allowed = max(1, max_teams_allowed - 2) 
    # --- FIM DA REMOÇÃO ---

    state.team_count_slider.max = max_teams_allowed
    state.team_count_slider.divisions = divisions_allowed
    current_value = min(state.preferred_team_count, max_teams_allowed)
    current_value = max(state.team_count_slider.min, min(current_value, state.team_count_slider.max))
    state.team_count_slider.value = current_value
    state.team_count_text.value = get_string(state, "teams_count", count=int(current_value))
    state.team_count_slider.on_change = update_team_count_text_and_save

    # --- Layout da View (API 0.28.3) ---
    view = ft.Column(
        [
            # Header
            ft.Row(
                [
                    ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main")), # API 0.28.3: String
                    ft.Text(
                        get_string(state, "selection_title"), 
                        size=20, 
                        weight="bold", 
                        expand=True, 
                        text_align=ft.TextAlign.CENTER
                    ), 
                    state.theme_toggle_button if state.theme_toggle_button else ft.Container(width=48)
                ], 
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            # Contador e Botão Limpar
            ft.Row(
                [
                    state.selected_count_text, 
                    ft.ElevatedButton( # Revertido para ElevatedButton como no original
                        get_string(state, "clear_button"), 
                        on_click=clear_selection
                    )
                ], 
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(), 
            state.checkbox_list, # Lista de jogadores (ListView)
            ft.Divider(),
            # Seletor de Times e Botão Organizar
            ft.Column(
                [
                    state.team_count_text, 
                    state.team_count_slider, 
                    ft.ElevatedButton( # Revertido para ElevatedButton
                        get_string(state, "organize_button_text"), 
                        icon="group", # API 0.28.3: String
                        on_click=lambda e: state.navigate_to("results"), 
                        width=350, 
                        height=40
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                spacing=10
            ),
        ], 
        expand=True, 
        spacing=5, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return view