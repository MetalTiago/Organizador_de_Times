# views/manage_players_view.py
import flet as ft
# Importa a nova função e as bibliotecas necessárias para as imagens
from db_handler import get_all_players, get_players_by_list, update_players_in_list, get_list_name
import os
import base64

class PlayerCheckboxItem(ft.Row):
    def __init__(self, player_data, is_selected):
        super().__init__()
        self.player_id = player_data[0]
        self.selected = is_selected
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        
        self.indicator_strip = ft.Container(
            width=5, height=55,
            bgcolor=ft.colors.PRIMARY if is_selected else None,
            border_radius=4
        )
        
        # --- LÓGICA DO AVATAR (FOTO) ---
        avatar_display = ft.Container(
            width=40, height=40,
            content=ft.Icon(ft.icons.PERSON_OUTLINE),
            border_radius=20
        )
        photo_path = player_data[3]
        if photo_path:
            try:
                with open(os.path.join("assets", photo_path), "rb") as f:
                    image_base64 = base64.b64encode(f.read()).decode('utf-8')
                avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=20)
            except:
                # Se o arquivo de imagem não for encontrado, mantém o ícone padrão
                pass
        
        # Usamos a propriedade 'leading' do ListTile para posicionar o avatar
        list_tile = ft.ListTile(
            title=ft.Text(player_data[1]),
            leading=avatar_display
        )
        
        self.content_container = ft.Container(
            content=list_tile,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.PRIMARY) if is_selected else None,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE))),
            border_radius=8,
            expand=True,
            on_click=self.toggle
        )
        
        self.controls = [self.indicator_strip, self.content_container]

    def toggle(self, e):
        self.selected = not self.selected
        self.indicator_strip.bgcolor = ft.colors.PRIMARY if self.selected else None
        self.content_container.bgcolor = ft.colors.with_opacity(0.05, ft.colors.PRIMARY) if self.selected else None
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

    def save_changes(e):
        final_member_ids = [item.player_id for item in all_checkbox_items if item.selected]
        try:
            update_players_in_list(state.active_list_id, final_member_ids)
            state.page.snack_bar = ft.SnackBar(ft.Text("Lista atualizada com sucesso!"), bgcolor=ft.colors.GREEN_700)
            state.page.snack_bar.open = True
            state.navigate_to("main")
        except Exception as ex:
            state.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {ex}"), bgcolor=ft.colors.RED_700)
            state.page.snack_bar.open = True
            state.update()

    # --- CORREÇÃO DO TÍTULO ---
    # Busca o nome diretamente do banco de dados, de forma segura
    active_list_name = get_list_name(state.active_list_id) if state.active_list_id != 0 else ""

    header = ft.Row(
        [
            ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main"), tooltip="Voltar"),
            ft.Row(
                [
                    ft.Text("Gerenciando a Lista:", size=16),
                    ft.Text(f'"{active_list_name}"', size=16, weight="bold", color=ft.colors.PRIMARY),
                    ft.IconButton(
                        icon=ft.icons.EDIT_OUTLINED,
                        on_click=lambda e: state.open_rename_list_dialog(e),
                        tooltip="Renomear Lista",
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
            ft.Row([ft.FilledButton("Salvar Alterações", icon=ft.icons.SAVE, on_click=save_changes, expand=True, height=50)], alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True
    )
    return view