# views/manage_players_view.py
import flet as ft
# import asyncio # <-- REMOVIDO
from db_handler import get_all_players, get_players_by_list, update_players_in_list, get_list_name
import os
import base64
from localization import get_string
from components import apply_opacity # Importa helper

APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".organizador_de_times")

class PlayerCheckboxItem(ft.Row):
    def __init__(self, player_data, is_selected):
        super().__init__()
        self.player_id = player_data[0]
        self.selected = is_selected
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        
        self.indicator_strip = ft.Container(width=5, height=55, bgcolor="primary" if is_selected else None, border_radius=4)
        avatar_display = ft.Container(width=40, height=40, content=ft.Icon("person_outline"), border_radius=20)
        
        photo_path = player_data[3]
        if photo_path:
            try:
                full_path = os.path.join(APP_DATA_DIR, photo_path)
                
                with open(full_path, "rb") as f:
                    image_base64 = base64.b64encode(f.read()).decode('utf-8')
                avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=20)
            except:
                pass
        
        self.player_name_text = ft.Text(player_data[1], color="primary" if is_selected else None)
        list_tile = ft.ListTile(title=self.player_name_text, leading=avatar_display)
        self.content_container = ft.Container(content=list_tile, bgcolor=apply_opacity("primary", 0.05) if is_selected else None, border=ft.border.only(bottom=ft.BorderSide(1, apply_opacity("on_surface", 0.1))), border_radius=8, expand=True, on_click=self.toggle)
        
        self.controls = [self.indicator_strip, self.content_container]

    def toggle(self, e):
        self.selected = not self.selected
        self.indicator_strip.bgcolor = "primary" if self.selected else None
        self.content_container.bgcolor = apply_opacity("primary", 0.05) if self.selected else None
        self.player_name_text.color = "primary" if self.selected else None
        self.update()

def build_manage_players_view(state):
    """Constrói a view para gerenciar quais jogadores estão em uma lista."""
    all_players = get_all_players()
    players_in_list = get_players_by_list(state.active_list_id)
    members_ids = {player[0] for player in players_in_list}
    
    players_checkbox_list = ft.ListView(expand=True, spacing=0, padding=0)
    all_checkbox_items = []

    for player in all_players:
        item = PlayerCheckboxItem(player_data=player, is_selected=(player[0] in members_ids))
        players_checkbox_list.controls.append(item)
        all_checkbox_items.append(item)

    def save_changes(e): # <--- Revertido para 'def'
        final_member_ids = [item.player_id for item in all_checkbox_items if item.selected]
        try:
            update_players_in_list(state.active_list_id, final_member_ids)
            
            # --- CORREÇÃO (on_dismiss) ---
            def on_snack_dismiss(e):
                state.navigate_to("main")
                # state.update() # navigate_to já chama update()

            snack_bar = ft.SnackBar(
                ft.Text(get_string(state, "list_updated_success")), 
                bgcolor="green_700",
            )
            snack_bar.on_dismiss = on_snack_dismiss # <--- Atribuído como propriedade
            state.page.snack_bar = snack_bar
            snack_bar.open = True
            state.update() # Mostra a SnackBar
            # --- FIM DA CORREÇÃO ---

        except Exception as ex:
            state.page.snack_bar = ft.SnackBar(
                ft.Text(get_string(state, "save_error", error=ex)), 
                bgcolor="red_700"
            )
            state.page.snack_bar.open = True
            state.update()

    active_list_name = get_list_name(state.active_list_id) if state.active_list_id != 0 else ""

    header = ft.Row(
        [
            ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main"), tooltip=get_string(state, "back_button_tooltip")),
            ft.Row(
                [
                    ft.Text(get_string(state, "manage_list_title"), size=16),
                    ft.Text(f'"{active_list_name}"', size=16, weight="bold", color="primary"),
                    ft.IconButton(
                        icon="edit_outlined", # Nome do ícone
                        on_click=lambda e: state.open_rename_list_dialog(e),
                        tooltip=get_string(state, "rename_list_tooltip"),
                        icon_size=20,
                    )
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(width=40)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    view = ft.Column(
        controls=[
            header,
            ft.Divider(),
            players_checkbox_list,
            ft.Divider(),
            ft.Row([ft.FilledButton(
                get_string(state, "save_changes_button"), 
                icon="save", 
                on_click=save_changes, # <--- Revertido
                expand=True, 
                height=50
            )], alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True
    )
    return view
