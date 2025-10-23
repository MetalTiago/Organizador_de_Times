# views/results_view.py
import flet as ft
# Usa ft.colors.
from organizer import organizar_times
import asyncio
import os
import base64
from localization import get_string, get_team_color_name
# REMOVIDO: import ads_manager

cores_times_hex = ["#D32F2F","#1976D2","#388E3C","#FBC02D","#7B1FA2","#F57C00","#0097A7","#C2185B","#689F38","#303F9F",]
async def share_teams(state, teams_data):
    text_to_copy = get_string(state, "results_title") + ":\n\n"
    for i, team_data in enumerate(teams_data):
        nome_cor = get_team_color_name(state, i)
        text_to_copy += f"{get_string(state, 'team_name_prefix', color_name=nome_cor)}:\n"
        for player in sorted(team_data, key=lambda x: x[1]): text_to_copy += f"- {player[1]}\n"
        text_to_copy += "\n"
    state.page.set_clipboard(text_to_copy)
    state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "all_teams_copied_success")), bgcolor=ft.colors.BLUE_700); state.page.snack_bar.open = True; state.page.update() # Usa ft.colors.

async def share_single_team(state, team_data, team_name):
    text_to_copy = f"{team_name}:\n"
    for player in sorted(team_data, key=lambda x: x[1]): text_to_copy += f"- {player[1]}\n"
    state.page.set_clipboard(text_to_copy)
    state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "team_copied_success", team_name=team_name)), bgcolor=ft.colors.BLUE_700); state.page.snack_bar.open = True; state.page.update() # Usa ft.colors.


def build_results_view(state):
    # Removido: organization_granted_by_ad = False
    is_initial_organization = True # Flag para permitir a primeira organização gratuita

    def update_team_cards_layout():
        team_cards = []
        for i, team_data in enumerate(state.resultado_times):
            nome_cor = get_team_color_name(state, i)
            valor_cor_hex = cores_times_hex[i % len(cores_times_hex)]
            team_name_str = get_string(state, "team_name_prefix", color_name=nome_cor)

            players_column = ft.Column(spacing=8)
            for j in sorted(team_data, key=lambda x: x[1]):
                avatar_display = ft.Container(width=28, height=28, content=ft.Icon(name="person_outline", size=16), border_radius=14, bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE)) # Usa ft.colors.
                if len(j) > 3 and j[3]:
                    photo_path = j[3]; image_base64 = state.photo_cache.get(j[0])
                    if not image_base64 and photo_path:
                         try:
                             full_photo_path = os.path.join("assets", photo_path)
                             if os.path.exists(full_photo_path):
                                 with open(full_photo_path, "rb") as f: image_base64 = base64.b64encode(f.read()).decode('utf-8'); state.photo_cache[j[0]] = image_base64
                             else: print(f"Warning: Photo not found at {full_photo_path}")
                         except Exception as img_ex: image_base64 = None; print(f"Error loading image {photo_path}: {img_ex}")
                    if image_base64: avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=14)
                players_column.controls.append(ft.Row([avatar_display, ft.Text(f"{j[1]}", size=14)], spacing=10))

            team_cards.append(ft.Container( content=ft.Card(elevation=4, margin=0, content=ft.Column([ ft.Container( content=ft.Row([ ft.Text(team_name_str, weight="bold", size=16, color=ft.colors.WHITE, expand=True, text_align=ft.TextAlign.CENTER), ft.IconButton( icon="share", icon_color=ft.colors.WHITE, icon_size=18, tooltip=get_string(state, "copy_button_tooltip", team_name=team_name_str), on_click=lambda _, t=team_data, n=team_name_str: state.page.run_task(share_single_team, state, t, n) ) ]), bgcolor=valor_cor_hex, padding=ft.padding.only(left=15, right=5, top=8, bottom=8), border_radius=ft.border_radius.only(top_left=8, top_right=8) ), ft.Container( content=ft.Column([ players_column, ft.Divider(height=5, color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE)), ft.Row([ ft.Text(get_string(state, "total_skill_label"), weight="bold"), ft.Text(f"{sum(p[2] for p in team_data)}", weight="bold") ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ], spacing=10), padding=12 ) ], spacing=0)), expand=True )) # Usa ft.colors.

        state.teams_layout_container.controls.clear()
        for i in range(0, len(team_cards), 2): state.teams_layout_container.controls.append(ft.Row(controls=team_cards[i:i+2], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START))
        state.update()

    async def _perform_organization():
        nonlocal is_initial_organization # Usa apenas esta flag agora
        page = state.page
        message = get_string(state, "reorganizing_dialog_title") if state.resultado_times else get_string(state, "organizing_dialog_title")
        if page.dialog and page.dialog.open: page.dialog.open = False; page.update(); await asyncio.sleep(0.1)
        page.dialog = ft.AlertDialog(title=ft.Text(message), modal=True)
        page.dialog.open = True; page.update()
        await asyncio.sleep(0.5)
        num_teams = int(state.team_count_slider.value) if state.team_count_slider.value else 2
        state.resultado_times = organizar_times(state.selecionados, num_teams)
        if page.dialog: page.dialog.open = False
        update_team_cards_layout()
        is_initial_organization = False # Marca que a inicial já ocorreu

    # Removido: _on_reward_granted_async()

    async def reorganize_teams_click(page: ft.Page, e=None):
        nonlocal is_initial_organization

        # Se for Pro OU foi a primeira organização
        if state.is_pro or is_initial_organization:
            print("Organizando (Pro ou Inicial)...")
            await _perform_organization()
        else:
            # --- MOSTRA DIÁLOGO SUGERINDO UPGRADE PRO ---
            if page.dialog and page.dialog.open: page.dialog.open = False; page.update(); await asyncio.sleep(0.1)

            page.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(get_string(state, "daily_organization_limit_reached_title")),
                content=ft.Text(get_string(state, "daily_organization_limit_reached_message")), # Mensagem ajustada
                actions=[
                    ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(page.dialog, 'open', False) or page.update()),
                    ft.ElevatedButton(get_string(state, "upgrade_button"), on_click=lambda _: state.navigate_to("settings")) # Botão Upgrade
                    # Removido: Botão Assistir Anúncio
                ],
                actions_alignment=ft.MainAxisAlignment.END # Alinha botões à direita
            )
            page.dialog.open = True
            page.update()

    async def share_all_teams_click(e):
        if state.is_pro:
            if state.resultado_times: await share_teams(state, state.resultado_times)
            else: state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "generate_teams_first_error")), bgcolor=ft.colors.RED_700); state.page.snack_bar.open = True; state.update() # Usa ft.colors.
        else:
            state.page.show_dialog(ft.AlertDialog(
                 title=ft.Text(get_string(state, "feature_for_pro_title")),
                 content=ft.Text(get_string(state, "sharing_pro_feature_message")),
                 actions=[ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.update()),
                          ft.ElevatedButton(get_string(state, "upgrade_button"), on_click=lambda _: state.navigate_to("settings"))]
            ))
            state.update()

    view = ft.Column([
        ft.Row([ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("selection")), ft.Text(get_string(state, "results_title"), size=24, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), state.theme_toggle_button if state.theme_toggle_button else ft.Container(width=48)], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([
                ft.ElevatedButton(get_string(state, "reorganize_button"), icon="refresh", on_click=lambda e: state.page.run_task(reorganize_teams_click, state.page)),
                ft.ElevatedButton(get_string(state, "share_all_button"), icon="share", on_click=share_all_teams_click)
               ],
               alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        state.teams_layout_container # Container onde os cards dos times serão adicionados
    ], expand=True)

    # Chama a organização inicial AQUI
    if state.page and callable(reorganize_teams_click):
        print("Chamando organização inicial...")
        state.page.run_task(reorganize_teams_click, state.page, None)

    return view