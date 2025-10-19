# views/main_view.py
import flet as ft
from db_handler import get_all_lists, create_list, delete_list, rename_list, get_list_name
from components import atualizar_tabela
from localization import get_string

def build_main_view(state):

    def update_menu_state():
        is_all_view = (state.active_list_id == 0)

        if hasattr(state, 'rename_menu_item') and state.rename_menu_item is not None:
            state.rename_menu_item.disabled = is_all_view
            state.manage_menu_item.disabled = is_all_view
            state.delete_menu_item.disabled = is_all_view
            state.list_management_menu.update()

        if hasattr(state, 'organize_button') and state.organize_button is not None:
            state.organize_button.disabled = is_all_view
            state.organize_button.tooltip = get_string(state, "organize_button_tooltip_disabled") if is_all_view else get_string(state, "organize_button_text")
            state.organize_button.update()

    def on_list_change(e):
        new_list_id = int(e.control.value)
        if new_list_id != state.active_list_id: # Salva apenas se mudou
            state.active_list_id = new_list_id
            state.save_last_list_preference(state.active_list_id)
            update_menu_state()
            atualizar_tabela(state)

    def populate_lists_dropdown():
        all_lists = get_all_lists()
        options = [ft.dropdown.Option(key=list_id, text=list_name) for list_id, list_name in all_lists]
        options.insert(0, ft.dropdown.Option(key=0, text=get_string(state, "all_players_list_name")))
        state.lists_dropdown.options = options
        state.lists_dropdown.value = str(state.active_list_id) # Dropdown value needs to be string
        update_menu_state() # Chama para definir o estado inicial dos botões/tooltips
    state.populate_lists_dropdown = populate_lists_dropdown

    def open_new_list_dialog(e):
        new_list_name = ft.TextField(label=get_string(state, "new_list_name_label"), autofocus=True)
        def save_new_list(e):
            if new_list_name.value:
                try:
                    list_id = create_list(new_list_name.value) # Pega o ID da nova lista
                    state.page.dialog.open = False
                    state.active_list_id = list_id # Define a nova lista como ativa
                    state.save_last_list_preference(list_id) # Salva a preferência
                    populate_lists_dropdown() # Atualiza o dropdown
                    atualizar_tabela(state) # Atualiza a tabela (mostrará vazia)
                except Exception as ex: # Captura erro específico se possível (ex: UNIQUE constraint)
                    new_list_name.error_text = get_string(state, "list_already_exists_error")
                    state.page.dialog.update()
        state.page.dialog = ft.AlertDialog(
            title=ft.Text(get_string(state, "create_list_dialog_title")),
            content=new_list_name,
            actions=[
                ft.TextButton(get_string(state, "save_button"), on_click=save_new_list),
                ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.page.update())
            ]
        )
        state.page.dialog.open = True
        state.update()

    # --- CORREÇÃO AQUI: A DEFINIÇÃO DA FUNÇÃO VEM PRIMEIRO ---
    def open_rename_list_dialog(e):
        if state.active_list_id == 0: return
        current_name = get_list_name(state.active_list_id)
        new_list_name_edit = ft.TextField(label=get_string(state, "new_list_name_label_edit"), value=current_name, autofocus=True)
        def save_new_name(e):
            if new_list_name_edit.value and new_list_name_edit.value.strip() and new_list_name_edit.value != current_name:
                try:
                    rename_list(state.active_list_id, new_list_name_edit.value.strip())
                    state.page.dialog.open = False
                    populate_lists_dropdown() # Atualiza o dropdown com o novo nome
                    state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "list_renamed_success")), bgcolor=ft.colors.GREEN)
                    state.page.snack_bar.open = True
                    state.page.update()
                except Exception: # Captura erro (ex: nome já existe)
                    new_list_name_edit.error_text = get_string(state, "list_already_exists_error")
                    state.page.dialog.update()

        state.page.dialog = ft.AlertDialog(
            title=ft.Text(get_string(state, "rename_list_dialog_title")),
            content=new_list_name_edit,
            actions=[
                ft.TextButton(get_string(state, "save_button"), on_click=save_new_name),
                ft.TextButton(get_string(state, "cancel_button"), on_click=lambda e: setattr(state.page.dialog, 'open', False) or state.page.update())
            ]
        )
        state.page.dialog.open = True
        state.update()
    # --- CORREÇÃO AQUI: A ATRIBUIÇÃO VEM DEPOIS DA DEFINIÇÃO ---
    state.open_rename_list_dialog = open_rename_list_dialog # Guarda a referência da função


    def manage_players_click(e):
        if state.active_list_id == 0: return
        state.navigate_to("manage_players")

    def delete_current_list(e):
        if state.active_list_id == 0: return
        if len(state.lists_dropdown.options) <= 2:
            state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "cannot_delete_last_list_error")), bgcolor=ft.colors.RED)
            state.page.snack_bar.open = True
            state.update()
            return
        list_name = get_list_name(state.active_list_id)
        def confirm_delete(e):
            delete_list(state.active_list_id)
            state.active_list_id = 0 # Volta para "Jogadores Cadastrados"
            state.save_last_list_preference(0) # Salva a preferência
            state.page.dialog.open = False
            populate_lists_dropdown() # Atualiza dropdown
            atualizar_tabela(state) # Atualiza tabela
        state.page.dialog = ft.AlertDialog(
            title=ft.Text(get_string(state, "delete_confirmation_title")),
            content=ft.Text(get_string(state, "delete_list_confirmation_content", list_name=list_name)),
            actions=[
                ft.TextButton(get_string(state, "yes_button"), on_click=confirm_delete, style=ft.ButtonStyle(color=ft.colors.RED)),
                ft.TextButton(get_string(state, "no_button"), on_click=lambda e: setattr(state.page.dialog, 'open', False) or state.page.update())
            ]
        )
        state.page.dialog.open = True
        state.update()

    def start_new_selection(e):
        state.selecionados.clear()
        state.photo_cache.clear()
        state.navigate_to("selection")

    state.lists_dropdown.on_change = on_list_change
    state.filter_name_input.label = get_string(state, "filter_by_name_label")
    state.filter_name_input.on_change = lambda e: atualizar_tabela(state, apply_filters=True)

    state.rename_menu_item = ft.PopupMenuItem(text=get_string(state, "rename_list_menu"), icon=ft.icons.EDIT, on_click=open_rename_list_dialog)
    state.manage_menu_item = ft.PopupMenuItem(text=get_string(state, "manage_players_menu"), icon=ft.icons.TUNE, on_click=manage_players_click)
    state.delete_menu_item = ft.PopupMenuItem(text=get_string(state, "delete_list_menu"), icon=ft.icons.DELETE_FOREVER, on_click=delete_current_list)
    state.list_management_menu = ft.PopupMenuButton(
        icon=ft.icons.MORE_VERT,
        items=[
            ft.PopupMenuItem(text=get_string(state, "create_new_list_menu"), icon=ft.icons.ADD, on_click=open_new_list_dialog),
            state.rename_menu_item,
            state.manage_menu_item,
            ft.PopupMenuItem(), # Separador
            state.delete_menu_item
        ]
    )

    state.organize_button = ft.ElevatedButton(
        get_string(state, "organize_button_text"),
        icon=ft.icons.GROUP_ADD,
        on_click=start_new_selection,
        expand=True
    )

    main_view_content = ft.Column(
        [
            ft.Column([
                ft.Text(get_string(state, "select_list_label"), weight="bold", size=14),
                ft.Row([state.lists_dropdown, state.list_management_menu]),
            ], spacing=5),
            ft.Divider(),
            ft.ResponsiveRow(
                [
                    ft.Container(content=state.organize_button, col={"xs": 12, "sm": 6}),
                    ft.Container(content=ft.ElevatedButton(get_string(state, "register_player_button_text"), icon=ft.icons.PERSON_ADD, on_click=lambda e: state.show_form(), expand=True), col={"xs": 12, "sm": 6}),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Divider(),
            ft.Row([state.filter_name_input]),
            ft.Stack( # Stack para loading indicator
                [
                    state.lista_jogadores,
                    ft.Container(
                        content=state.loading_indicator,
                        alignment=ft.alignment.center
                    )
                ],
                expand=True
            )
        ],
        spacing=10, expand=True
    )
    state.main_view_content = main_view_content

    app_bar_actions = ft.Row([
        state.theme_toggle_button,
        ft.IconButton(icon=ft.icons.SETTINGS_OUTLINED, tooltip=get_string(state, "settings_tooltip"), on_click=lambda _: state.navigate_to("settings"))
    ])

    view = ft.Column(
        [
            ft.Container( # Cabeçalho
                content=ft.Row(
                    [
                        ft.Image(src="icon_android.jpg", width=35, height=35, border_radius=6),
                        ft.Text(get_string(state, "app_title"), size=24, weight="bold", expand=True, text_align=ft.TextAlign.CENTER),
                        app_bar_actions,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.only(left=15, right=10, top=8, bottom=8),
                bgcolor=ft.colors.with_opacity(0.03, ft.colors.ON_SURFACE),
                border_radius=8,
                margin=ft.margin.only(bottom=10)
            ),
            state.input_container,
            state.edit_container,
            main_view_content
        ],
        expand=True
    )

    return view