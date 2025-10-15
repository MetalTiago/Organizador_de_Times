# views/selection_view.py
import flet as ft
from db_handler import get_players_by_list
import base64
import os

def build_selection_view(state):
    def update_selected_count():
         state.selected_count_text.value = f"Jogadores selecionados: {len(state.selecionados)}"

    def toggle_selection(jogador, indicator, container):
        is_selected = any(s[0] == jogador[0] for s in state.selecionados)
        if is_selected:
            state.selecionados[:] = [s for s in state.selecionados if s[0] != jogador[0]]
            indicator.visible = False; container.bgcolor = None
        else:
            state.selecionados.append(jogador)
            indicator.visible = True; container.bgcolor = ft.colors.with_opacity(0.05, ft.colors.PRIMARY)
        update_selected_count(); state.update()

    def montar_lista_jogadores():
        state.checkbox_list.controls.clear()
        users = get_players_by_list(state.active_list_id)
        for jogador in users:
            is_selected = any(s[0] == jogador[0] for s in state.selecionados)
            avatar_display = ft.Container(
                width=44, height=44, content=ft.Icon(ft.icons.PERSON_OUTLINE),
                border_radius=22, bgcolor=ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE)
            )
            player_id, photo_path = jogador[0], jogador[3]
            if photo_path:
                image_base64 = state.photo_cache.get(player_id)
                if not image_base64:
                    try:
                        with open(os.path.join("assets", photo_path), "rb") as f:
                            image_base64 = base64.b64encode(f.read()).decode('utf-8')
                            state.photo_cache[player_id] = image_base64
                    except: image_base64 = None
                if image_base64:
                    avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER)
            indicator_strip = ft.Container(width=5, height=55, bgcolor=ft.colors.PRIMARY, border_radius=4, visible=is_selected)
            list_tile = ft.ListTile(title=ft.Text(jogador[1]), leading=avatar_display)
            content_container = ft.Container(content=list_tile, bgcolor=ft.colors.with_opacity(0.05, ft.colors.PRIMARY) if is_selected else None, border=ft.border.only(bottom=ft.BorderSide(1, ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE))), border_radius=8, expand=True)
            list_tile.on_click = lambda e, j=jogador, i=indicator_strip, c=content_container: toggle_selection(j, i, c)
            state.checkbox_list.controls.append(ft.Row([indicator_strip, content_container], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER))
        update_selected_count()
    state.montar_lista_jogadores = montar_lista_jogadores

    def clear_selection(e):
        state.selecionados.clear(); montar_lista_jogadores(); state.update()

    def update_team_count_text(e):
        state.team_count_text.value = f"{int(e.control.value)} Times"; state.update()
    state.team_count_slider.on_change = update_team_count_text

    view = ft.Column([
        ft.Row([ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main")), ft.Text("Selecionar Jogadores", size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), state.theme_toggle_button], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([state.selected_count_text, ft.ElevatedButton("Limpar", on_click=clear_selection)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(), state.checkbox_list, ft.Divider(),
        ft.Column([state.team_count_text, state.team_count_slider, ft.ElevatedButton("Organizar Times", icon=ft.icons.GROUP, on_click=lambda e: state.navigate_to("results"), width=350, height=40)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
    ], expand=True, spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    return view