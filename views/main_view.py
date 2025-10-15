# views/main_view.py
import flet as ft
from db_handler import get_all_lists, create_list, delete_list, rename_list, get_list_name
from components import atualizar_tabela

def build_main_view(state):
    
    def update_menu_state():
        is_all_view = (state.active_list_id == 0)
        if hasattr(state, 'rename_menu_item') and state.rename_menu_item is not None:
            state.rename_menu_item.disabled = is_all_view
            state.manage_menu_item.disabled = is_all_view
            state.delete_menu_item.disabled = is_all_view
            state.list_management_menu.update()

    def on_list_change(e):
        state.active_list_id = int(e.control.value)
        update_menu_state()
        atualizar_tabela(state)

    def populate_lists_dropdown():
        all_lists = get_all_lists()
        options = [ft.dropdown.Option(key=list_id, text=list_name) for list_id, list_name in all_lists]
        options.insert(0, ft.dropdown.Option(key=0, text="Jogadores Cadastrados"))
        state.lists_dropdown.options = options
        state.lists_dropdown.value = state.active_list_id
        update_menu_state()
    state.populate_lists_dropdown = populate_lists_dropdown

    def open_new_list_dialog(e):
        new_list_name = ft.TextField(label="Nome da Nova Lista", autofocus=True)
        def save_new_list(e):
            if new_list_name.value:
                try:
                    create_list(new_list_name.value)
                    state.page.dialog.open = False
                    populate_lists_dropdown()
                    atualizar_tabela(state)
                except:
                    new_list_name.error_text = "Esta lista já existe."
                    state.page.dialog.update()
        state.page.dialog = ft.AlertDialog(title=ft.Text("Criar Nova Lista"), content=new_list_name, actions=[ft.TextButton("Salvar", on_click=save_new_list), ft.TextButton("Cancelar", on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.page.update())])
        state.page.dialog.open = True
        state.update()

    def open_rename_list_dialog(e):
        if state.active_list_id == 0: return 
        current_name = get_list_name(state.active_list_id)
        new_list_name_edit = ft.TextField(label="Novo nome da lista", value=current_name, autofocus=True)
        def save_new_name(e):
            if new_list_name_edit.value and new_list_name_edit.value != current_name:
                rename_list(state.active_list_id, new_list_name_edit.value)
                state.page.dialog.open = False
                populate_lists_dropdown()
                state.page.snack_bar = ft.SnackBar(ft.Text("Lista renomeada com sucesso!"), bgcolor=ft.colors.GREEN)
                state.page.snack_bar.open = True
                state.page.update()
        state.page.dialog = ft.AlertDialog(title=ft.Text("Renomear Lista"), content=new_list_name_edit, actions=[ft.TextButton("Salvar", on_click=save_new_name), ft.TextButton("Cancelar", on_click=lambda e: setattr(state.page.dialog, 'open', False) or state.page.update())])
        state.page.dialog.open = True
        state.update()

    def manage_players_click(e):
        if state.active_list_id == 0: return
        state.navigate_to("manage_players")

    def delete_current_list(e):
        if state.active_list_id == 0: return
        if len(state.lists_dropdown.options) <= 2:
            state.page.snack_bar = ft.SnackBar(ft.Text("Não é possível apagar a última lista."), bgcolor=ft.colors.RED)
            state.page.snack_bar.open = True
            state.update()
            return
        list_text = get_list_name(state.active_list_id)
        def confirm_delete(e):
            delete_list(state.active_list_id)
            state.active_list_id = 0
            state.page.dialog.open = False
            populate_lists_dropdown()
            atualizar_tabela(state)
        state.page.dialog = ft.AlertDialog(title=ft.Text("Confirmar Exclusão"), content=ft.Text(f"Tem certeza que deseja apagar a lista '{list_text}'?"), actions=[ft.TextButton("Sim, apagar", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.colors.RED)), ft.TextButton("Cancelar", on_click=lambda e: setattr(state.page.dialog, 'open', False) or state.page.update())])
        state.page.dialog.open = True
        state.update()

    def start_new_selection(e):
        if state.active_list_id == 0:
            state.page.snack_bar = ft.SnackBar(ft.Text("Crie ou selecione uma lista específica para organizar times."), bgcolor=ft.colors.ORANGE_700)
            state.page.snack_bar.open = True
            state.update()
            return
        state.selecionados.clear()
        state.photo_cache.clear()
        state.navigate_to("selection")

    state.lists_dropdown.on_change = on_list_change
    state.filter_name_input.on_change = lambda e: atualizar_tabela(state, apply_filters=True)

    state.rename_menu_item = ft.PopupMenuItem(text="Renomear lista atual", icon=ft.icons.EDIT, on_click=open_rename_list_dialog)
    state.manage_menu_item = ft.PopupMenuItem(text="Gerenciar Jogadores", icon=ft.icons.TUNE, on_click=manage_players_click)
    state.delete_menu_item = ft.PopupMenuItem(text="Excluir lista atual", icon=ft.icons.DELETE_FOREVER, on_click=delete_current_list)
    state.list_management_menu = ft.PopupMenuButton(
        icon=ft.icons.MORE_VERT,
        items=[
            ft.PopupMenuItem(text="Criar nova lista", icon=ft.icons.ADD, on_click=open_new_list_dialog),
            state.rename_menu_item,
            state.manage_menu_item,
            ft.PopupMenuItem(),
            state.delete_menu_item
        ]
    )
    
    main_view_content = ft.Column(
        [
            ft.Row([state.lists_dropdown, state.list_management_menu]),
            ft.Divider(),
            ft.ResponsiveRow([ft.Container(content=ft.ElevatedButton("Organizar Times", icon=ft.icons.GROUP_ADD, on_click=start_new_selection, expand=True), col={"xs": 12, "sm": 6}), ft.Container(content=ft.ElevatedButton("Cadastrar Jogador", icon=ft.icons.PERSON_ADD, on_click=lambda e: state.show_form(), expand=True), col={"xs": 12, "sm": 6}),], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(), ft.Row([state.filter_name_input]), ft.Row([state.loading_indicator], alignment=ft.MainAxisAlignment.CENTER),
            state.lista_jogadores,
        ],
        spacing=10, expand=True
    )
    state.main_view_content = main_view_content
    
    app_bar_actions = ft.Row([state.theme_toggle_button, ft.IconButton(icon=ft.icons.SETTINGS_OUTLINED, tooltip="Configurações", on_click=lambda _: state.navigate_to("settings"))])
    
    view = ft.Column(
        [
            ft.Row([ft.Icon(ft.icons.GROUPS_OUTLINED, size=30), ft.Text("Organizador de Times", size=26, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), app_bar_actions], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            state.input_container,
            state.edit_container,
            main_view_content
        ],
        expand=True
    )
    
    return view