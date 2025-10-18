# views/results_view.py
import flet as ft
from organizer import organizar_times
import asyncio
import os
import base64
from localization import get_string # Importa a função

cores_times = [
    ("Vermelho", "#D32F2F"), ("Azul", "#1976D2"), ("Verde", "#388E3C"),
    ("Amarelo", "#FBC02D"), ("Roxo", "#7B1FA2"), ("Laranja", "#F57C00"),
    ("Ciano", "#0097A7"), ("Rosa", "#C2185B"), ("Verde Limão", "#689F38"),
    ("Índigo", "#303F9F"),
]

async def share_teams(state, teams_data):
    text_to_copy = get_string(state, "results_title") + ":\n\n"
    for i, team_data in enumerate(teams_data):
        nome_cor, _ = cores_times[i % len(cores_times)]
        text_to_copy += f"{get_string(state, 'team_name_prefix', color_name=nome_cor)}:\n"
        for player in sorted(team_data, key=lambda x: x[1]): text_to_copy += f"- {player[1]}\n"
        text_to_copy += "\n"
    state.page.set_clipboard(text_to_copy)
    state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "all_teams_copied_success")), bgcolor=ft.colors.BLUE_700); state.page.snack_bar.open = True; state.page.update()

async def share_single_team(state, team_data, team_name):
    text_to_copy = f"{team_name}:\n"
    for player in sorted(team_data, key=lambda x: x[1]): text_to_copy += f"- {player[1]}\n"
    state.page.set_clipboard(text_to_copy)
    state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "team_copied_success", team_name=team_name)), bgcolor=ft.colors.BLUE_700); state.page.snack_bar.open = True; state.page.update()

def build_results_view(state):
    def update_team_cards_layout():
        team_cards = []
        for i, team_data in enumerate(state.resultado_times):
            nome_cor, valor_cor = cores_times[i % len(cores_times)]
            team_name_str = get_string(state, "team_name_prefix", color_name=nome_cor)
            players_column = ft.Column(spacing=8)
            for j in sorted(team_data, key=lambda x: x[1]):
                avatar_display = ft.Container(width=28, height=28, content=ft.Icon(ft.icons.PERSON_OUTLINE, size=16), border_radius=14, bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE))
                if j[3]:
                    image_base64 = state.photo_cache.get(j[0])
                    if image_base64: avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER)
                players_column.controls.append(ft.Row([avatar_display, ft.Text(f"{j[1]}", size=14)], spacing=10))
            team_cards.append(ft.Container(content=ft.Card(elevation=4, margin=0, content=ft.Column([ft.Container(content=ft.Row([ft.Text(team_name_str, weight="bold", size=16, color=ft.colors.WHITE, expand=True, text_align=ft.TextAlign.CENTER), ft.IconButton(icon=ft.icons.SHARE, icon_color=ft.colors.WHITE, icon_size=18, tooltip=get_string(state, "copy_button_tooltip", team_name=team_name_str), on_click=lambda _, t=team_data, n=team_name_str: state.page.run_task(share_single_team, state, t, n))]), bgcolor=valor_cor, padding=ft.padding.only(left=15, right=5, top=8, bottom=8), border_radius=ft.border_radius.only(top_left=8, top_right=8)), ft.Container(content=ft.Column([players_column, ft.Divider(height=5, color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE)), ft.Row([ft.Text(get_string(state, "total_skill_label"), weight="bold"), ft.Text(f"{sum(j[2] for j in team_data)}", weight="bold")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)], spacing=10), padding=12)], spacing=0)), expand=True))
        
        state.teams_layout_container.controls.clear()
        for i in range(0, len(team_cards), 2):
            state.teams_layout_container.controls.append(ft.Row(controls=team_cards[i:i+2], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START))
        state.update()

    async def reorganize_teams_click(e=None):
        message = get_string(state, "reorganizing_dialog_title") if state.resultado_times else get_string(state, "organizing_dialog_title")
        state.page.dialog = ft.AlertDialog(title=ft.Text(message), modal=True); state.page.dialog.open = True; state.update()
        await asyncio.sleep(0.5)
        state.resultado_times = organizar_times(state.selecionados, int(state.team_count_slider.value))
        state.page.dialog.open = False
        update_team_cards_layout()

    async def share_all_teams_click(e):
        if state.resultado_times: await share_teams(state, state.resultado_times)
        else: state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "generate_teams_first_error")), bgcolor=ft.colors.RED_700); state.page.snack_bar.open = True; state.update()

    state.reorganize_teams = reorganize_teams_click

    view = ft.Column([
        ft.Row([ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("selection")), ft.Text(get_string(state, "results_title"), size=24, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), state.theme_toggle_button]),
        ft.Row([ft.ElevatedButton(get_string(state, "reorganize_button"), icon=ft.icons.REFRESH, on_click=reorganize_teams_click), ft.ElevatedButton(get_string(state, "share_all_button"), icon=ft.icons.SHARE, on_click=share_all_teams_click)], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        state.teams_layout_container
    ], expand=True)
    return view