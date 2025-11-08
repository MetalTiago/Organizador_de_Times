# views/main_view.py
import flet as ft
# import asyncio # <-- REMOVIDO
from db_handler import (get_all_lists, create_list, delete_list, rename_list,
                        get_list_name, count_custom_lists) 
from components import (atualizar_tabela, apply_opacity, 
                        build_input_container, build_edit_container)
from localization import get_string

def build_main_view(state):
    
    state.input_container = build_input_container(state)
    state.edit_container = build_edit_container(state)

    def update_menu_state():
        is_all_view = (state.active_list_id == 0)
        if hasattr(state, 'rename_menu_item') and state.rename_menu_item is not None:
            state.rename_menu_item.disabled = is_all_view
            state.manage_menu_item.disabled = is_all_view
            state.delete_menu_item.disabled = is_all_view
            if hasattr(state, 'list_management_menu') and state.list_management_menu: state.list_management_menu.update()
        if hasattr(state, 'organize_button') and state.organize_button is not None:
            state.organize_button.disabled = is_all_view
            state.organize_button.tooltip = get_string(state, "organize_button_tooltip_disabled") if is_all_view else get_string(state, "organize_button_text")
            if state.organize_button: state.organize_button.update()

    def on_list_change(e):
        new_list_id = int(e.control.value)
        if new_list_id != state.active_list_id:
            state.active_list_id = new_list_id
            state.save_last_list_preference(state.active_list_id)
            update_menu_state()
            atualizar_tabela(state)

    def populate_lists_dropdown():
        all_lists = get_all_lists()
        options = [ft.dropdown.Option(key=str(list_id), text=list_name) for list_id, list_name in all_lists]
        options.insert(0, ft.dropdown.Option(key="0", text=get_string(state, "all_players_list_name")))
        state.lists_dropdown.options = options
        valid_keys = [opt.key for opt in options]
        current_value = str(state.active_list_id) if str(state.active_list_id) in valid_keys else "0"
        if current_value == "0" and state.active_list_id != 0: 
             state.active_list_id = 0
             state.save_last_list_preference(0) 
        state.lists_dropdown.value = current_value
        update_menu_state() 
    state.populate_lists_dropdown = populate_lists_dropdown

    def open_new_list_dialog(e):
        new_list_name = ft.TextField(label=get_string(state, "new_list_name_label"), autofocus=True)

        dialog = ft.AlertDialog(
            title=ft.Text(get_string(state, "create_list_dialog_title")),
            content=new_list_name,
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=10)
        )

        def save_new_list(e): # <--- Revertido para 'def'
            list_name_value = new_list_name.value.strip()
            if list_name_value:
                try:
                    list_id = create_list(list_name_value)
                    state.page.close(dialog) 
                    state.active_list_id = list_id
                    state.save_last_list_preference(list_id)
                    populate_lists_dropdown()
                    atualizar_tabela(state)
                except Exception as ex:
                    print(f"Erro ao criar lista: {ex}")
                    if "UNIQUE constraint failed" in str(ex): new_list_name.error_text = get_string(state, "list_already_exists_error")
                    else: new_list_name.error_text = f"Erro: {ex}"
                    state.page.update() # <--- update SÍNCRONO
        
        dialog.actions = [
            ft.TextButton(get_string(state, "save_button"), on_click=save_new_list), # <--- Revertido
            ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: state.page.close(dialog)) 
        ]
        state.page.open(dialog) 

    def open_rename_list_dialog(e):
        if state.active_list_id == 0: return
        current_name = get_list_name(state.active_list_id)
        new_list_name_edit = ft.TextField(label=get_string(state, "new_list_name_label_edit"), value=current_name, autofocus=True)
        
        dialog = ft.AlertDialog(
            title=ft.Text(get_string(state, "rename_list_dialog_title")),
            content=new_list_name_edit,
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        
        def save_new_name(e): # <--- Revertido para 'def'
            new_name_value = new_list_name_edit.value.strip()
            if new_name_value and new_name_value != current_name:
                try:
                    rename_list(state.active_list_id, new_name_value)
                    state.page.close(dialog) 
                    
                    # --- CORREÇÃO (on_dismiss) ---
                    def on_snack_dismiss(e):
                        if state.page.route == "/manage_players":
                            state.navigate_to("manage_players")
                        else:
                            populate_lists_dropdown()
                            state.page.update()
                    
                    snack_bar = ft.SnackBar(
                        ft.Text(get_string(state, "list_renamed_success")), 
                        bgcolor="green_700",
                    )
                    snack_bar.on_dismiss = on_snack_dismiss # <--- Atribuído como propriedade
                    state.page.snack_bar = snack_bar
                    snack_bar.open = True
                    state.update() # Mostra a SnackBar
                    # --- FIM DA CORREÇÃO ---
                        
                except Exception as ex:
                     print(f"Erro ao renomear lista: {ex}")
                     if "UNIQUE constraint failed" in str(ex): new_list_name_edit.error_text = get_string(state, "list_already_exists_error")
                     else: new_list_name_edit.error_text = f"Erro: {ex}"
                     state.page.update() # update SÍNCRONO
        
        dialog.actions = [
            ft.TextButton(get_string(state, "save_button"), on_click=save_new_name), # <--- Revertido
            ft.TextButton(get_string(state, "cancel_button"), on_click=lambda e: state.page.close(dialog))
        ]
        state.page.open(dialog)
    
    state.open_rename_list_dialog = open_rename_list_dialog

    def manage_players_click(e):
        if state.active_list_id == 0: return
        state.navigate_to("manage_players")

    def delete_current_list(e):
        if state.active_list_id == 0: return
        if len(state.lists_dropdown.options) <= 2:
            state.page.snack_bar = ft.SnackBar(
                ft.Text(get_string(state, "cannot_delete_last_list_error")), 
                bgcolor="red_700"
            )
            state.page.snack_bar.open = True
            state.update()
            return 
        
        list_name = get_list_name(state.active_list_id)

        dialog = ft.AlertDialog(
            title=ft.Text(get_string(state, "delete_confirmation_title")),
            content=ft.Text(get_string(state, "delete_list_confirmation_content", list_name=list_name)),
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=10)
        )

        def confirm_delete(e):
            state.page.close(dialog)
            try:
                delete_list(state.active_list_id); state.active_list_id = 0; state.save_last_list_preference(0)
                populate_lists_dropdown(); atualizar_tabela(state)
            except Exception as del_ex: print(f"Erro ao deletar lista: {del_ex}")
            finally: state.update() 
        
        dialog.actions = [
            ft.TextButton(get_string(state, "yes_button"), on_click=confirm_delete, style=ft.ButtonStyle(color="red")),
            ft.TextButton(get_string(state, "no_button"), on_click=lambda e: state.page.close(dialog))
        ]
        state.page.open(dialog)

    def start_new_selection(e): state.selecionados.clear(); state.photo_cache.clear(); state.navigate_to("selection")

    state.lists_dropdown.on_change = on_list_change
    state.filter_name_input.label = get_string(state, "filter_by_name_label")
    state.filter_name_input.on_change = lambda e: atualizar_tabela(state, apply_filters=True)

    state.rename_menu_item = ft.PopupMenuItem(text=get_string(state, "rename_list_menu"), icon="edit", on_click=open_rename_list_dialog)
    state.manage_menu_item = ft.PopupMenuItem(text=get_string(state, "manage_players_menu"), icon="tune", on_click=manage_players_click)
    state.delete_menu_item = ft.PopupMenuItem(text=get_string(state, "delete_list_menu"), icon="delete_forever", on_click=delete_current_list)
    state.list_management_menu = ft.PopupMenuButton( icon="more_vert", items=[ ft.PopupMenuItem(text=get_string(state, "create_new_list_menu"), icon="add", on_click=open_new_list_dialog), state.rename_menu_item, state.manage_menu_item, ft.PopupMenuItem(), state.delete_menu_item ] )
    state.organize_button = ft.ElevatedButton( get_string(state, "organize_button_text"), icon="group_add", on_click=start_new_selection, expand=True )

    main_view_content = ft.Column( [ ft.Column([ ft.Text(get_string(state, "select_list_label"), weight="bold", size=14), ft.Row([state.lists_dropdown, state.list_management_menu]), ], spacing=5), ft.Divider(), ft.ResponsiveRow([ ft.Container(content=state.organize_button, col={"xs": 12, "sm": 6}), ft.Container(content=ft.ElevatedButton(get_string(state, "register_player_button_text"), icon="person_add", on_click=lambda e: state.show_form(), expand=True), col={"xs": 12, "sm": 6}), ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER), ft.Divider(), ft.Row([state.filter_name_input]), ft.Stack([ ft.Container( content=state.loading_indicator, alignment=ft.alignment.center, expand=True ), state.lista_jogadores, ], expand=True ) ], spacing=10, expand=True )
    
    state.main_view_content = main_view_content

    app_bar_actions = ft.Row([ state.theme_toggle_button, ft.IconButton(icon="settings", tooltip=get_string(state, "settings_tooltip"), on_click=lambda _: state.navigate_to("settings")) ])

    view = ft.Column( [ ft.Container( content=ft.Row([ ft.Image(src="icon_android.jpg", width=35, height=35, border_radius=6), ft.Text(get_string(state, "app_title"), size=24, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), app_bar_actions, ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,), padding=ft.padding.only(left=15, right=10, top=8, bottom=8), bgcolor=apply_opacity("on_surface", 0.03), border_radius=8, margin=ft.margin.only(bottom=10) ), 
        state.input_container, 
        state.edit_container, 
        main_view_content 
    ], expand=True ) 
    
    return view
