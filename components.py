# components.py
import flet as ft
import os
import shutil
import base64
# import asyncio # <-- REMOVIDO
from db_handler import (get_players_by_list, delete_player, update_player,
                        add_player_to_list, insert_player, get_all_players,
                        get_all_lists, count_all_players) 
from localization import get_string

state = None

APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".organizador_de_times")

def set_page_ref(_state):
    global state; state = _state

def apply_opacity(color_constant: str, opacity: float) -> str:
    opacity = max(0.0, min(1.0, opacity))
    return f"{color_constant},{opacity}"

def build_input_container(app_state):
    name_input = ft.TextField(label=get_string(app_state, "player_name_label"), autofocus=True)
    skill_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}", expand=True)
    img_preview_bgcolor = apply_opacity("on_surface", 0.1) 
    img_preview = ft.Container(width=80, height=80, content=ft.Icon(name="person", size=40), border_radius=40, bgcolor=img_preview_bgcolor)
    lists_checkbox_group = ft.Column(scroll=ft.ScrollMode.AUTO)

    def populate_lists_checkboxes():
        lists_checkbox_group.controls.clear()
        all_lists = get_all_lists()
        name_input.value = ""
        skill_slider.value = 0
        skill_text.value = "0"
        img_preview.content = ft.Icon(name="person", size=40)
        img_preview.data = None
        for list_id, list_name in all_lists:
            is_checked = (list_id == app_state.active_list_id and app_state.active_list_id != 0)
            lists_checkbox_group.controls.append(ft.Checkbox(label=list_name, value=is_checked, data=list_id))
    app_state.populate_new_player_lists_form = populate_lists_checkboxes

    def file_picker_result(e: ft.FilePickerResultEvent): # <--- Revertido para 'def'
        if e.files:
            selected_file = e.files[0]
            upload_dir = os.path.join(APP_DATA_DIR, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            dest_path_full = os.path.join(upload_dir, selected_file.name)
            try:
                shutil.copy(selected_file.path, dest_path_full)
                relative_path = os.path.join("uploads", selected_file.name).replace("\\", "/")
                img_preview.data = relative_path
                with open(dest_path_full, "rb") as f: image_base64 = base64.b64encode(f.read()).decode('utf-8')
                img_preview.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=40)
            except Exception as copy_error: print(f"Erro ao copiar/ler imagem: {copy_error}")
            app_state.page.update() # <--- update() síncrono
            
    if app_state.input_file_picker:
        app_state.input_file_picker.on_result = file_picker_result # <--- Revertido

    def save_user(e): # <--- Revertido para 'def'
        if not name_input.value:
             name_input.error_text = get_string(app_state, "name_cannot_be_empty_error")
             app_state.page.update(); return
        selected_list_ids = [cb.data for cb in lists_checkbox_group.controls if cb.value]
        if not selected_list_ids:
             app_state.page.snack_bar = ft.SnackBar(
                 ft.Text(get_string(app_state, "select_at_least_one_list_error")), 
                 bgcolor="red_700"
             )
             app_state.page.snack_bar.open = True
             app_state.page.update()
             return 
        try:
             player_id = insert_player(name_input.value, int(skill_slider.value), img_preview.data)
             for list_id in selected_list_ids: add_player_to_list(list_id, player_id)
             
             # --- CORREÇÃO (on_dismiss) ---
             # Define a ação que acontece APÓS a SnackBar fechar
             def on_snack_dismiss(e):
                atualizar_tabela(app_state)
                app_state.hide_form()
                # app_state.update() # app_state.hide_form() já chama update()
             
             snack_bar = ft.SnackBar(
                 ft.Text(get_string(app_state, "player_saved_success")), 
                 bgcolor="green_700"
                 # on_dismiss no construtor removido
             )
             snack_bar.on_dismiss = on_snack_dismiss # <--- Atribuído como propriedade
             app_state.page.snack_bar = snack_bar
             snack_bar.open = True
             app_state.update() # Mostra a SnackBar (hide_form() foi movido para o on_dismiss)
             # --- FIM DA CORREÇÃO ---
             
        except Exception as ex:
             app_state.page.snack_bar = ft.SnackBar(
                 ft.Text(get_string(app_state, "generic_error", error=ex)), 
                 bgcolor="red_700"
             )
             app_state.page.snack_bar.open = True
             app_state.page.update()

    skill_text = ft.Text("0")
    skill_slider.on_change = lambda e: setattr(skill_text, 'value', f"{int(e.control.value):n}") or app_state.update()

    def pick_input_file(e): # <--- Revertido para 'def'
        if app_state.input_file_picker:
            app_state.input_file_picker.pick_files( # <--- Revertido para 'pick_files'
                allow_multiple=False, 
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        else:
            print("Input file picker não inicializado")

    choose_photo_button = ft.TextButton(
        get_string(app_state, "choose_photo_button"), 
        icon="upload_file", 
        on_click=pick_input_file # <--- Revertido
    )

    input_card = ft.Card( visible=False, elevation=10, content=ft.Container(padding=20, content=ft.Column( [ ft.Row([ft.Text(get_string(app_state, "new_player_title"), size=20, weight="bold"), ft.IconButton(icon="close", icon_size=25, on_click=lambda e: app_state.hide_form())], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Row([ ft.Column([img_preview, choose_photo_button], horizontal_alignment=ft.CrossAxisAlignment.CENTER), ft.Column([name_input, ft.Row([ft.Text(get_string(app_state, "skill_label")), skill_text])], expand=True) ], alignment=ft.CrossAxisAlignment.START), skill_slider, ft.Divider(), ft.Text(get_string(app_state, "add_to_lists_label"), weight="bold"), ft.Container( content=lists_checkbox_group, height=150, border=ft.border.all(1, apply_opacity("on_surface", 0.2)), border_radius=8, padding=ft.padding.symmetric(horizontal=10) ), ft.Container(content=ft.FilledButton(
        get_string(app_state, "save_player_button"), 
        on_click=save_user, # <--- Revertido
        icon="save"), alignment=ft.alignment.center, padding=10) ], scroll=ft.ScrollMode.ADAPTIVE )) ) 
    return input_card

def build_edit_container(app_state):
    name_edit = ft.TextField(label=get_string(app_state, "player_name_label"))
    skill_edit = ft.Slider(min=0, max=10, divisions=10, label="{value}", expand=True)
    img_edit_bgcolor = apply_opacity("on_surface", 0.1) 
    img_preview_edit = ft.Container(width=80, height=80, content=ft.Icon(name="person", size=40), border_radius=40, bgcolor=img_edit_bgcolor)
    id_edit = ft.Text(); skill_text_edit = ft.Text("0")

    def file_picker_result_edit(e: ft.FilePickerResultEvent): # <--- Revertido para 'def'
        if e.files:
            selected_file = e.files[0]; 
            upload_dir = os.path.join(APP_DATA_DIR, "uploads"); 
            os.makedirs(upload_dir, exist_ok=True)
            dest_path_full = os.path.join(upload_dir, selected_file.name)
            try:
                shutil.copy(selected_file.path, dest_path_full); relative_path = os.path.join("uploads", selected_file.name).replace("\\", "/")
                img_preview_edit.data = relative_path
                with open(dest_path_full, "rb") as f: image_base64 = base64.b64encode(f.read()).decode('utf-8')
                img_preview_edit.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=40)
            except Exception as copy_error: print(f"Erro ao copiar/ler imagem (edit): {copy_error}")
            app_state.page.update() # <--- update() síncrono

    if app_state.edit_file_picker:
        app_state.edit_file_picker.on_result = file_picker_result_edit # <--- Revertido

    def hide_edit_form(): app_state.edit_container.visible = False; app_state.main_view_content.visible = True; app_state.update()

    def update_and_save_user(e): # <--- Revertido para 'def'
        
        # --- CORREÇÃO (on_dismiss) ---
        def on_snack_dismiss(e):
            hide_edit_form()
            atualizar_tabela(app_state)
            # app_state.update() # hide_edit_form() já chama update()

        update_player(int(id_edit.value), name_edit.value, int(skill_edit.value), img_preview_edit.data)
        
        snack_bar = ft.SnackBar(
            ft.Text(get_string(app_state, "player_updated_success")), 
            bgcolor="green_700"
            # on_dismiss REMOVIDO do construtor
        )
        snack_bar.on_dismiss = on_snack_dismiss # <--- Atribuído como propriedade
        app_state.page.snack_bar = snack_bar
        snack_bar.open = True
        app_state.update() # Mostra a SnackBar
        # --- FIM DA CORREÇÃO ---

    skill_edit.on_change = lambda e: setattr(skill_text_edit, 'value', f"{int(e.control.value):n}") or app_state.update()

    def pick_edit_file(e): # <--- Revertido para 'def'
        if app_state.edit_file_picker:
            app_state.edit_file_picker.pick_files( # <--- Revertido para 'pick_files'
                allow_multiple=False, 
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        else:
            print("Edit file picker não inicializado")
            
    change_photo_button = ft.TextButton(
        get_string(app_state, "change_photo_button"), 
        icon="upload_file", 
        on_click=pick_edit_file # <--- Revertido
    )

    edit_container = ft.Card( visible=False, elevation=10, content=ft.Container(padding=20, content=ft.Column([ ft.Row([ft.Text(get_string(app_state, "edit_player_title"), size=20, weight="bold"), ft.IconButton(icon="close", icon_size=25, on_click=lambda e: hide_edit_form())], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Row([ ft.Column([img_preview_edit, change_photo_button], horizontal_alignment=ft.CrossAxisAlignment.CENTER), ft.Column([name_edit, ft.Row([ft.Text(get_string(app_state, "skill_label")), skill_text_edit])], expand=True) ], alignment=ft.CrossAxisAlignment.START), skill_edit, ft.Container(content=ft.FilledButton(
        get_string(app_state, "update_button"), 
        on_click=update_and_save_user, # <--- Revertido
        icon="save"), alignment=ft.alignment.center, padding=10) ], scroll=ft.ScrollMode.ADAPTIVE)) )

    def show_edit_form(user_data):
        id_edit.value = str(user_data["id"]); name_edit.value = user_data["name"]
        skill_edit.value = float(user_data["skill"]); skill_text_edit.value = str(int(skill_edit.value))
        img_preview_edit.data = None; img_preview_edit.content = ft.Icon(name="person", size=40)
        if user_data["photo_path"]:
             full_photo_path_edit = os.path.join(APP_DATA_DIR, user_data["photo_path"])
             if os.path.exists(full_photo_path_edit):
                 try:
                     with open(full_photo_path_edit, "rb") as f: image_base64 = base64.b64encode(f.read()).decode('utf-8')
                     img_preview_edit.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=40); img_preview_edit.data = user_data["photo_path"]
                 except Exception as img_load_err: print(f"Erro ao carregar imagem existente (edit): {img_load_err}"); img_preview_edit.content = ft.Icon(name="person", size=40)
             else: print(f"Aviso: Imagem salva não encontrada em {full_photo_path_edit}"); img_preview_edit.content = ft.Icon(name="person", size=40)
        app_state.edit_container.visible = True; app_state.main_view_content.visible = False; app_state.update()
    app_state.show_edit_form = show_edit_form
    return edit_container

def atualizar_tabela(app_state, apply_filters=False):
    list_id = app_state.active_list_id
    app_state.loading_indicator.visible = True; app_state.lista_jogadores.visible = False; app_state.update()
    app_state.lista_jogadores.controls.clear()
    users = get_all_players() if list_id == 0 else get_players_by_list(list_id)
    if apply_filters: name_filter = app_state.filter_name_input.value.lower() if app_state.filter_name_input.value else ""; users = [user for user in users if name_filter in user[1].lower()]

    if not users:
        is_all_players_view = (list_id == 0)
        empty_state_component = ft.Container( content=ft.Column( [ ft.Icon(name="person_search", size=60, color=apply_opacity("on_surface", 0.4)), ft.Text(get_string(app_state, "empty_state_title"), size=18, weight="bold"), ft.Text(get_string(app_state, "empty_state_subtitle1"), size=14, color=apply_opacity("on_surface", 0.8), text_align=ft.TextAlign.CENTER), ft.Text(get_string(app_state, "empty_state_subtitle2"), size=14, color=apply_opacity("on_surface", 0.8), visible=not is_all_players_view, text_align=ft.TextAlign.CENTER), ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, opacity=0.8, ), padding=ft.padding.symmetric(vertical=50, horizontal=10), alignment=ft.alignment.center ) 
        app_state.lista_jogadores.controls.append(empty_state_component)
    else:
        for user in users:
            user_dict = {"id": user[0], "name": user[1], "skill": user[2], "photo_path": user[3]}; skill_color = cor_skill(user_dict["skill"])
            avatar_display = ft.Container(width=40, height=40, content=ft.Icon(name="person_outline"), border_radius=20, bgcolor=skill_color)
            if user_dict["photo_path"]:
                 full_photo_path_list = os.path.join(APP_DATA_DIR, user_dict["photo_path"])
                 if os.path.exists(full_photo_path_list):
                     try:
                         with open(full_photo_path_list, "rb") as f: image_base64 = base64.b64encode(f.read()).decode('utf-8')
                         avatar_display.content = ft.Image(src_base64=image_base64, fit=ft.ImageFit.COVER, border_radius=20)
                     except Exception as img_list_err: print(f"Erro ao carregar imagem na lista: {img_list_err}"); avatar_display.content = ft.Icon(name="person_outline")
                 else: avatar_display.content = ft.Icon(name="person_outline")

            list_item = ft.Container( content=ft.Row( [ avatar_display, ft.Column([ ft.Text(user_dict["name"], weight="bold"), ft.Text(f"{get_string(state, 'skill_label')} {user_dict['skill']}", color=skill_color) ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True), ft.Row([ 
                ft.IconButton(icon="edit", icon_color="blue_400", data=user_dict, on_click=lambda e: app_state.show_edit_form(e.control.data), tooltip=get_string(app_state, "edit_tooltip")), 
                ft.IconButton(icon="delete", icon_color="red_400", data=user_dict["id"], on_click=lambda e: showdelete_confirm(app_state, e.control.data), tooltip=get_string(app_state, "delete_tooltip")) 
                ]) ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=15 ), padding=ft.padding.symmetric(vertical=10, horizontal=15), border=ft.border.only(bottom=ft.BorderSide(1, apply_opacity("on_surface", 0.1))), ) 
            app_state.lista_jogadores.controls.append(list_item)

    app_state.loading_indicator.visible = False; app_state.lista_jogadores.visible = True; app_state.update()

def cor_skill(n):
    n = int(n)
    if n <= 4: return apply_opacity("on_surface", 0.8) 
    if 4 < n < 7: return "redaccent_400"
    elif 6 < n < 9: return "yellowaccent_400"
    elif n >= 9: return "lightblueaccent_400"
    return "on_surface" 

def showdelete_confirm(app_state, player_id):
    
    confirm_delete_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(get_string(app_state, "delete_confirmation_title")),
        content=ft.Text(get_string(app_state, "delete_player_confirmation_content")),
        shape=ft.RoundedRectangleBorder(radius=10)
    )

    def confirm_action(e): # <--- Revertido para 'def'
        app_state.page.close(confirm_delete_dialog) 
        
        if e.control.text == get_string(app_state, "yes_button"):
            
            # --- CORREÇÃO (on_dismiss) ---
            def on_snack_dismiss(e):
                delete_player(player_id) 
                atualizar_tabela(app_state)
                # app_state.update() # atualizar_tabela() já chama update()

            snack_bar = ft.SnackBar(
                ft.Text(get_string(app_state, "player_deleted_success")), 
                bgcolor="green_700"
                # on_dismiss REMOVIDO do construtor
            )
            snack_bar.on_dismiss = on_snack_dismiss # <--- Atribuído como propriedade
            app_state.page.snack_bar = snack_bar
            snack_bar.open = True
            app_state.update() # Mostra a SnackBar
            # --- FIM DA CORREÇÃO ---
        else:
            app_state.update() 

    confirm_delete_dialog.actions = [
        ft.TextButton(get_string(app_state, "yes_button"), on_click=confirm_action, style=ft.ButtonStyle(color="red")), # <--- Revertido
        ft.TextButton(get_string(app_state, "no_button"), on_click=confirm_action) # <--- Revertido
    ]
    
    app_state.page.open(confirm_delete_dialog)