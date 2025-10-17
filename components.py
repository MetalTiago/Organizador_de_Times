# components.py
import flet as ft
import os
import shutil
import base64
from db_handler import get_players_by_list, delete_player, update_player, add_player_to_list, insert_player, get_all_players, get_all_lists

state = None

def set_page_ref(_state):
    global state; state = _state

def build_input_container(app_state):
    name_input = ft.TextField(label="Nome", autofocus=True)
    skill_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}", expand=True)
    img_preview = ft.Container(width=80, height=80, content=ft.Icon(ft.icons.PERSON, size=40), border_radius=40, bgcolor=ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE))
    
    lists_checkbox_group = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    def populate_lists_checkboxes():
        lists_checkbox_group.controls.clear()
        all_lists = get_all_lists()
        name_input.value = ""
        skill_slider.value = 0
        skill_text.value = "0"
        img_preview.content = ft.Icon(ft.icons.PERSON, size=40)
        img_preview.data = None
        
        for list_id, list_name in all_lists:
            is_checked = (list_id == app_state.active_list_id and app_state.active_list_id != 0)
            lists_checkbox_group.controls.append(ft.Checkbox(label=list_name, value=is_checked, data=list_id))
        
    app_state.populate_new_player_lists_form = populate_lists_checkboxes
    
    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            dest_path_full = os.path.join("assets/uploads", selected_file.name)
            shutil.copy(selected_file.path, dest_path_full)
            relative_path = os.path.join("uploads", selected_file.name).replace("\\", "/")
            img_preview.data = relative_path
            with open(selected_file.path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
            img_preview.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=40)
            app_state.update()
    file_picker = ft.FilePicker(on_result=file_picker_result)
    app_state.page.overlay.append(file_picker)

    def save_user(e):
        if not name_input.value:
            name_input.error_text = "O nome não pode estar vazio"
            state.update()
            return
        
        selected_list_ids = [cb.data for cb in lists_checkbox_group.controls if cb.value]
        
        if not selected_list_ids:
            state.page.snack_bar = ft.SnackBar(ft.Text("Selecione pelo menos uma lista!"), bgcolor=ft.colors.RED_700)
            state.page.snack_bar.open = True
            state.update()
            return

        try:
            player_id = insert_player(name_input.value, int(skill_slider.value), img_preview.data)
            for list_id in selected_list_ids:
                add_player_to_list(list_id, player_id)

            state.page.snack_bar = ft.SnackBar(ft.Text("Cadastrado com sucesso"), bgcolor=ft.colors.GREEN_700)
            state.page.snack_bar.open = True
            atualizar_tabela(state)
            state.hide_form()
        except Exception as ex:
            state.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao cadastrar: {ex}"), bgcolor=ft.colors.RED_700)
            state.page.snack_bar.open = True
            state.update()
    
    skill_text = ft.Text("0")
    skill_slider.on_change = lambda e: setattr(skill_text, 'value', f"{int(e.control.value):n}") or state.update()
    
    input_card = ft.Card(
        visible=False, elevation=10,
        content=ft.Container(padding=20, content=ft.Column(
            [
                ft.Row([ft.Text("Novo Jogador", size=20, weight="bold"), ft.IconButton(icon="close", icon_size=25, on_click=lambda e: state.hide_form())], alignment="spaceBetween"),
                ft.Row([
                    ft.Column([img_preview, ft.TextButton("Escolher Foto", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"]))], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([name_input, ft.Row([ft.Text("Skill:"), skill_text])], expand=True)
                ], alignment=ft.CrossAxisAlignment.START),
                skill_slider,
                ft.Divider(),
                ft.Text("Adicionar às Listas:", weight="bold"),
                ft.Container(
                    content=lists_checkbox_group,
                    height=150,
                    border=ft.border.all(1, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
                    border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10)
                ),
                ft.Container(content=ft.FilledButton("Salvar Jogador", on_click=save_user, icon=ft.icons.SAVE), alignment=ft.alignment.center, padding=10)
            ],
            scroll=ft.ScrollMode.ADAPTIVE
        ))
    )
    return input_card


def build_edit_container(app_state):
    name_edit = ft.TextField(label="Nome")
    skill_edit = ft.Slider(min=0, max=10, divisions=10, label="{value}", expand=True)
    img_preview_edit = ft.Container(width=80, height=80, content=ft.Icon(ft.icons.PERSON, size=40), border_radius=40, bgcolor=ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE))
    id_edit = ft.Text()
    skill_text_edit = ft.Text("0")
    
    def file_picker_result_edit(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            dest_path_full = os.path.join("assets/uploads", selected_file.name)
            shutil.copy(selected_file.path, dest_path_full)
            relative_path = os.path.join("uploads", selected_file.name).replace("\\", "/")
            img_preview_edit.data = relative_path
            with open(selected_file.path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
            img_preview_edit.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=40)
            app_state.update()
    file_picker_edit = ft.FilePicker(on_result=file_picker_result_edit)
    app_state.page.overlay.append(file_picker_edit)
    
    def hide_edit_form():
        app_state.edit_container.visible = False
        app_state.main_view_content.visible = True
        app_state.update()
    
    def update_and_save_user(e):
        update_player(int(id_edit.value), name_edit.value, int(skill_edit.value), img_preview_edit.data)
        hide_edit_form()
        atualizar_tabela(app_state)
        app_state.page.snack_bar = ft.SnackBar(ft.Text("Jogador atualizado!"), bgcolor=ft.colors.GREEN_700)
        app_state.page.snack_bar.open = True
        app_state.update()

    skill_edit.on_change = lambda e: setattr(skill_text_edit, 'value', f"{int(e.control.value):n}") or state.update()
    
    edit_container = ft.Card(
        visible=False, elevation=10,
        content=ft.Container(padding=20, content=ft.Column([
            ft.Row([ft.Text("Editar Jogador", size=20, weight="bold"), ft.IconButton(icon="close", icon_size=25, on_click=lambda e: hide_edit_form())], alignment="spaceBetween"),
            ft.Row([
                ft.Column([img_preview_edit, ft.TextButton("Mudar Foto", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: file_picker_edit.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"]))], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([name_edit, ft.Row([ft.Text("Skill:"), skill_text_edit])], expand=True)
            ], alignment=ft.CrossAxisAlignment.START),
            skill_edit,
            ft.Container(content=ft.FilledButton("Atualizar", on_click=update_and_save_user, icon=ft.icons.SAVE), alignment=ft.alignment.center, padding=10)
        ], scroll=ft.ScrollMode.ADAPTIVE))
    )
    
    def show_edit_form(user_data):
        id_edit.value = str(user_data["id"])
        name_edit.value = user_data["name"]
        skill_edit.value = float(user_data["skill"])
        skill_text_edit.value = str(int(skill_edit.value))
        if user_data["photo_path"]:
            try:
                with open(os.path.join("assets", user_data["photo_path"]), "rb") as f:
                    image_base64 = base64.b64encode(f.read()).decode('utf-8')
                img_preview_edit.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=40)
            except:
                img_preview_edit.content = ft.Icon(ft.icons.PERSON)
            img_preview_edit.data = user_data["photo_path"]
        else:
            img_preview_edit.content = ft.Icon(ft.icons.PERSON)
            img_preview_edit.data = None
        app_state.edit_container.visible = True
        app_state.main_view_content.visible = False
        app_state.update()
    
    app_state.show_edit_form = show_edit_form
    return edit_container

def atualizar_tabela(app_state, apply_filters=False):
    list_id = app_state.active_list_id
    
    app_state.loading_indicator.visible = True
    app_state.lista_jogadores.visible = False
    app_state.update()

    app_state.lista_jogadores.controls.clear()
    
    if list_id == 0: 
        users = get_all_players()
    else: 
        users = get_players_by_list(list_id)

    if apply_filters:
        name_filter = app_state.filter_name_input.value.lower() if app_state.filter_name_input.value else ""
        users = [user for user in users if name_filter in user[1].lower()]
        
    if not users:
        # --- ALTERAÇÃO AQUI ---
        is_all_players_view = (list_id == 0)
        
        empty_state_component = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.icons.SPORTS_SOCCER_OUTLINED, size=60, color=ft.colors.with_opacity(0.4, ft.colors.ON_SURFACE)),
                    ft.Text("Nenhum jogador por aqui...", size=18, weight="bold"),
                    ft.Text(
                        "Clique em 'Cadastrar Jogador' para adicionar o primeiro!",
                        size=14,
                        color=ft.colors.with_opacity(0.8, ft.colors.ON_SURFACE),
                        text_align=ft.TextAlign.CENTER
                    ),
                    # Adiciona a segunda instrução apenas se não estivermos na visão "Todos os Jogadores"
                    ft.Text(
                        "Ou use o menu (⋮) e 'Gerenciar Jogadores' para adicionar jogadores já existentes a esta lista.",
                        size=14,
                        color=ft.colors.with_opacity(0.8, ft.colors.ON_SURFACE),
                        visible=not is_all_players_view, # A instrução só aparece em listas específicas
                        text_align=ft.TextAlign.CENTER
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                opacity=0.8,
            ),
            padding=ft.padding.symmetric(vertical=50, horizontal=10),
            alignment=ft.alignment.center
        )
        # --- FIM DA ALTERAÇÃO ---
        app_state.lista_jogadores.controls.append(empty_state_component)
    else:
        for user in users:
            user_dict = {"id": user[0], "name": user[1], "skill": user[2], "photo_path": user[3]}
            avatar_display = ft.Container(
                width=40, height=40, content=ft.Icon(ft.icons.PERSON_OUTLINE),
                border_radius=20, bgcolor=cor_skill(user_dict["skill"])
            )
            if user_dict["photo_path"]:
                try:
                    with open(os.path.join("assets", user_dict["photo_path"]), "rb") as f:
                        image_base64 = base64.b64encode(f.read()).decode('utf-8')
                    avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER)
                except:
                    pass
            list_item = ft.Container(
                content=ft.Row(
                    [
                        avatar_display,
                        ft.Column([
                            ft.Text(user_dict["name"], weight="bold"),
                            ft.Text(f"Skill: {user_dict['skill']}", color=cor_skill(user_dict["skill"]))
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                        ft.Row([
                            ft.IconButton(icon=ft.icons.EDIT, icon_color=ft.colors.BLUE_400, data=user_dict, on_click=lambda e: state.show_edit_form(e.control.data), tooltip="Editar"),
                            ft.IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.RED_400, data=user_dict["id"], on_click=lambda e: showdelete_confirm(e.control.data), tooltip="Excluir")
                        ])
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                padding=ft.padding.symmetric(vertical=10, horizontal=15),
                border=ft.border.only(bottom=ft.BorderSide(1, ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE))),
            )
            app_state.lista_jogadores.controls.append(list_item)
            
    app_state.loading_indicator.visible = False
    app_state.lista_jogadores.visible = True
    app_state.update()

def cor_skill(n):
    n = int(n)
    if n <= 4: return ft.colors.with_opacity(0.8, ft.colors.ON_SURFACE)
    if 4 < n < 7: return ft.colors.RED_ACCENT_400
    elif 6 < n < 9: return ft.colors.YELLOW_ACCENT_400
    elif n >= 9: return ft.colors.LIGHT_BLUE_ACCENT_400
    return ft.colors.ON_SURFACE

confirm_delete_dialog = ft.AlertDialog(modal=True, title=ft.Text("Confirmação de Exclusão"), content=ft.Text("Tem certeza que deseja excluir este jogador?"))
def showdelete_confirm(player_id):
    def confirm_action(e):
        confirm_delete_dialog.open = False
        if e.control.text == "Sim":
            delete_player(player_id)
            atualizar_tabela(state)
            state.page.snack_bar = ft.SnackBar(ft.Text("Jogador excluído!"), bgcolor=ft.colors.GREEN_700)
            state.page.snack_bar.open = True
        state.update()
    
    confirm_delete_dialog.actions = [ft.TextButton("Sim", on_click=confirm_action, style=ft.ButtonStyle(color=ft.colors.RED)), ft.TextButton("Não", on_click=confirm_action)]
    state.page.dialog = confirm_delete_dialog
    confirm_delete_dialog.open = True
    state.update()