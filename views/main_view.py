# views/main_view.py
import flet as ft
# Usa ft.colors. (correto para 0.25.x)
from db_handler import (get_all_lists, create_list, delete_list, rename_list,
                        get_list_name, count_custom_lists) # Importa count_custom_lists
from components import atualizar_tabela
from localization import get_string

# Define o limite como uma constante
LIST_LIMIT_FREE = 2

def build_main_view(state):

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
        # Garante que o valor inicial do dropdown seja o ID carregado do estado
        # Verifica se o ID salvo ainda existe nas opções, senão volta para "0"
        valid_keys = [opt.key for opt in options]
        current_value = str(state.active_list_id) if str(state.active_list_id) in valid_keys else "0"
        if current_value == "0" and state.active_list_id != 0: # Se voltou para 0 porque a lista salva foi deletada
             state.active_list_id = 0
             state.save_last_list_preference(0) # Salva a preferência atualizada
        state.lists_dropdown.value = current_value
        update_menu_state() # Chama para definir o estado inicial dos botões/tooltips
    state.populate_lists_dropdown = populate_lists_dropdown

    def open_new_list_dialog(e):
        # --- VERIFICAÇÃO DE LIMITE DE LISTAS ---
        if not state.is_pro and count_custom_lists() >= LIST_LIMIT_FREE:
            state.page.show_dialog(ft.AlertDialog(
                 title=ft.Text(get_string(state, "limit_reached_title")),
                 content=ft.Text(get_string(state, "list_limit_reached_message", limit=LIST_LIMIT_FREE)),
                 actions=[
                     ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.update()),
                     ft.ElevatedButton(get_string(state, "upgrade_button"), on_click=lambda _: state.navigate_to("settings")) # Botão para ir às Configurações
                 ]
            ))
            state.update()
            return # Impede a abertura do diálogo de criação

        new_list_name = ft.TextField(label=get_string(state, "new_list_name_label"), autofocus=True)
        def save_new_list(e):
            list_name_value = new_list_name.value.strip()
            if list_name_value:
                try:
                    list_id = create_list(list_name_value)
                    state.page.dialog.open = False
                    state.active_list_id = list_id
                    state.save_last_list_preference(list_id)
                    populate_lists_dropdown()
                    atualizar_tabela(state)
                except Exception as ex:
                    print(f"Erro ao criar lista: {ex}")
                    if "UNIQUE constraint failed" in str(ex): new_list_name.error_text = get_string(state, "list_already_exists_error")
                    else: new_list_name.error_text = f"Erro: {ex}"
                    if state.page.dialog: state.page.dialog.update()

        state.page.dialog = ft.AlertDialog(
            title=ft.Text(get_string(state, "create_list_dialog_title")),
            content=new_list_name,
            actions=[ ft.TextButton(get_string(state, "save_button"), on_click=save_new_list), ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.update()) ]
        )
        state.page.dialog.open = True
        state.update()

    def open_rename_list_dialog(e):
        if state.active_list_id == 0: return
        current_name = get_list_name(state.active_list_id)
        new_list_name_edit = ft.TextField(label=get_string(state, "new_list_name_label_edit"), value=current_name, autofocus=True)
        def save_new_name(e):
            new_name_value = new_list_name_edit.value.strip()
            if new_name_value and new_name_value != current_name:
                try:
                    rename_list(state.active_list_id, new_name_value)
                    state.page.dialog.open = False
                    populate_lists_dropdown() # Atualiza o dropdown com o novo nome
                    state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "list_renamed_success")), bgcolor=ft.colors.GREEN_700) # Usa ft.colors.
                    state.page.snack_bar.open = True
                    state.page.update()
                except Exception as ex:
                     print(f"Erro ao renomear lista: {ex}")
                     if "UNIQUE constraint failed" in str(ex): new_list_name_edit.error_text = get_string(state, "list_already_exists_error")
                     else: new_list_name_edit.error_text = f"Erro: {ex}"
                     if state.page.dialog: state.page.dialog.update()
        state.page.dialog = ft.AlertDialog( title=ft.Text(get_string(state, "rename_list_dialog_title")), content=new_list_name_edit, actions=[ ft.TextButton(get_string(state, "save_button"), on_click=save_new_name), ft.TextButton(get_string(state, "cancel_button"), on_click=lambda e: setattr(state.page.dialog, 'open', False) or state.page.update()) ] )
        state.page.dialog.open = True
        state.update()
    state.open_rename_list_dialog = open_rename_list_dialog

    def manage_players_click(e):
        if state.active_list_id == 0: return
        state.navigate_to("manage_players")

    def delete_current_list(e):
        if state.active_list_id == 0: return
        # A opção "Todos" (key="0") sempre existe, então comparamos com 1 lista real + "Todos"
        if len(state.lists_dropdown.options) <= 2:
            state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "cannot_delete_last_list_error")), bgcolor=ft.colors.RED_700); state.page.snack_bar.open = True; state.update(); return # Usa ft.colors.
        list_name = get_list_name(state.active_list_id)
        def confirm_delete(e):
            try:
                delete_list(state.active_list_id); state.active_list_id = 0; state.save_last_list_preference(0)
                if state.page.dialog: state.page.dialog.open = False
                populate_lists_dropdown(); atualizar_tabela(state)
            except Exception as del_ex: print(f"Erro ao deletar lista: {del_ex}")
            finally: state.update() # Garante atualização da UI
        state.page.dialog = ft.AlertDialog( title=ft.Text(get_string(state, "delete_confirmation_title")), content=ft.Text(get_string(state, "delete_list_confirmation_content", list_name=list_name)), actions=[ ft.TextButton(get_string(state, "yes_button"), on_click=confirm_delete, style=ft.ButtonStyle(color=ft.colors.RED)), ft.TextButton(get_string(state, "no_button"), on_click=lambda e: setattr(state.page.dialog, 'open', False) or state.update()) ] ) # Usa ft.colors.
        state.page.dialog.open = True; state.update()

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

    view = ft.Column( [ ft.Container( content=ft.Row([ ft.Image(src="icon_android.jpg", width=35, height=35, border_radius=6), ft.Text(get_string(state, "app_title"), size=24, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), app_bar_actions, ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,), padding=ft.padding.only(left=15, right=10, top=8, bottom=8), bgcolor=ft.colors.with_opacity(0.03, ft.colors.ON_SURFACE), border_radius=8, margin=ft.margin.only(bottom=10) ), state.input_container, state.edit_container, main_view_content ], expand=True ) # Usa ft.colors.
    return view