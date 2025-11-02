# views/selection_view.py
import flet as ft
# Usa ft.colors.
from db_handler import get_players_by_list
import base64
import os
from localization import get_string

# --- CORREÇÃO DE COR ---
# Importa a sua função apply_opacity para corrigir ft.colors.with_opacity
from components import apply_opacity
# --- FIM DA CORREÇÃO ---

# Define o limite como constante (Vamos remover na Fase 1.5)
TEAM_LIMIT_FREE = 3

# --- CORREÇÃO (Etapa 2.2) ---
# Define o caminho de dados gravável, assim como o db_handler.py e components.py
APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".organizador_de_times")
# --- FIM DA CORREÇÃO ---

def build_selection_view(state):

    def update_selected_count():
         if state and hasattr(state, 'selected_count_text'):
             state.selected_count_text.value = get_string(state, "selected_players_count", count=len(state.selecionados))

    def toggle_selection(jogador, indicator, container, name_text):
        is_selected = any(s[0] == jogador[0] for s in state.selecionados)
        if is_selected:
            state.selecionados[:] = [s for s in state.selecionados if s[0] != jogador[0]]
            indicator.visible = False; container.bgcolor = None; name_text.color = None
        else:
            state.selecionados.append(jogador)
            # --- CORREÇÃO DE COR ---
            indicator.visible = True; container.bgcolor = apply_opacity("primary", 0.05); name_text.color = "primary" 
            # --- FIM DA CORREÇÃO ---
        update_selected_count(); state.update()

    def montar_lista_jogadores():
        state.checkbox_list.controls.clear()
        users = get_players_by_list(state.active_list_id)
        for jogador in users:
            is_selected = any(s[0] == jogador[0] for s in state.selecionados)
            
            # --- CORREÇÃO DE COR (Linha 32) ---
            avatar_display = ft.Container(width=44, height=44, content=ft.Icon(name="person_outline"), border_radius=22, bgcolor=apply_opacity("on_surface", 0.1)) 
            # --- FIM DA CORREÇÃO ---
            
            player_id, photo_path = jogador[0], jogador[3]
            if photo_path:
                image_base64 = state.photo_cache.get(player_id)
                if not image_base64:
                    try:
                        # --- CORREÇÃO (Etapa 2.2) ---
                        # Lê do diretório de dados do app, não de 'assets'
                        full_path = os.path.join(APP_DATA_DIR, photo_path)
                        # --- FIM DA CORREÇÃO ---
                        
                        if os.path.exists(full_path):
                            with open(full_path, "rb") as f: image_base64 = base64.b64encode(f.read()).decode('utf-8'); state.photo_cache[player_id] = image_base64
                    except Exception as img_err: image_base64 = None; print(f"Erro img selection: {img_err}")
                if image_base64: avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=22)

            # --- CORREÇÃO DE COR ---
            indicator_strip = ft.Container(width=5, height=55, bgcolor="primary", border_radius=4, visible=is_selected) 
            player_name_text = ft.Text(jogador[1], color="primary" if is_selected else None) 
            list_tile = ft.ListTile(title=player_name_text, leading=avatar_display)
            content_container = ft.Container(content=list_tile, bgcolor=apply_opacity("primary", 0.05) if is_selected else None, border=ft.border.only(bottom=ft.BorderSide(1, apply_opacity("on_surface", 0.1))), border_radius=8, expand=True) 
            # --- FIM DA CORREÇÃO ---
            
            list_tile.on_click = lambda e, j=jogador, i=indicator_strip, c=content_container, nt=player_name_text: toggle_selection(j, i, c, nt)
            state.checkbox_list.controls.append(ft.Row([indicator_strip, content_container], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER))
        update_selected_count()
    state.montar_lista_jogadores = montar_lista_jogadores

    def clear_selection(e): state.selecionados.clear(); montar_lista_jogadores(); state.update()

    def update_team_count_text_and_save(e):
        count = int(e.control.value)
        # --- (Esta é a Fase 1.5, removeremos esta verificação) ---
        max_teams = 10 # if state.is_pro else TEAM_LIMIT_FREE (Removido o if)
        if count > max_teams:
            count = max_teams
            state.team_count_slider.value = count 
            state.page.show_dialog(ft.AlertDialog(
                 title=ft.Text(get_string(state, "limit_reached_title")),
                 content=ft.Text(get_string(state, "team_limit_reached_message", limit=max_teams)),
                 actions=[
                     ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.update()),
                     ft.ElevatedButton(get_string(state, "upgrade_button"), on_click=lambda _: state.navigate_to("settings"))
                 ]
            ))
        # --- (Fim da Fase 1.5) ---

        state.team_count_text.value = get_string(state, "teams_count", count=count)
        state.save_last_team_count_preference(count) 
        state.update() 

    # --- (Ajuste da Fase 1.5) ---
    max_teams_allowed = 10 # if state.is_pro else TEAM_LIMIT_FREE (Removido o if)
    divisions_allowed = max(1, max_teams_allowed - 2) 
    # --- FIM DA CORREÇÃO ---

    state.team_count_slider.max = max_teams_allowed
    state.team_count_slider.divisions = divisions_allowed
    current_value = min(state.preferred_team_count, max_teams_allowed)
    current_value = max(state.team_count_slider.min, min(current_value, state.team_count_slider.max))
    state.team_count_slider.value = current_value
    state.team_count_text.value = get_string(state, "teams_count", count=int(current_value))
    state.team_count_slider.on_change = update_team_count_text_and_save

    view = ft.Column([
        ft.Row([ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main")), ft.Text(get_string(state, "selection_title"), size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), state.theme_toggle_button if state.theme_toggle_button else ft.Container(width=48)], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([state.selected_count_text, ft.ElevatedButton(get_string(state, "clear_button"), on_click=clear_selection)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(), state.checkbox_list, ft.Divider(),
        ft.Column([state.team_count_text, state.team_count_slider, ft.ElevatedButton(get_string(state, "organize_button_text"), icon="group", on_click=lambda e: state.navigate_to("results"), width=350, height=40)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
    ], expand=True, spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    return view