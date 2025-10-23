# views/settings_view.py
import flet as ft
# Usa ft.colors. diretamente (correto para Flet 0.25.x)
import csv
from db_handler import (
    get_all_player_list_associations, get_player_by_name, get_list_by_name,
    insert_player, update_player, create_list, add_player_to_list
)
from localization import get_string

def build_settings_view(state):
    """Constrói a view de Configurações."""

    # --- FUNÇÃO PARA MUDAR O IDIOMA ---
    def change_language(e):
        selected_lang_code = e.control.value
        if selected_lang_code != state.current_language:
            state.current_language = selected_lang_code # Atualiza estado interno primeiro
            state.save_language_preference(selected_lang_code) # Salva no config.json
            # Recarrega a view para aplicar traduções
            state.navigate_to("settings")
            # Atualiza o título da janela principal
            if state.page:
                state.page.title = get_string(state, "app_title")
                state.page.update()

    # --- CRIA O DROPDOWN DE IDIOMAS ---
    language_dropdown = ft.Dropdown(
        label=get_string(state, "language_selection_label"),
        value=state.current_language, # Usa o idioma carregado do estado
        options=[
            ft.dropdown.Option("pt_br", get_string(state, "language_pt_br")),
            ft.dropdown.Option("en_us", get_string(state, "language_en_us")),
            ft.dropdown.Option("es", get_string(state, "language_es")),
        ],
        on_change=change_language,
        expand=True
    )

    # --- Funções Placeholder para Compra/Desativação ---
    def buy_pro_click(e):
        """Chamada ao clicar em 'Tornar-se Pro'."""
        state.purchase_pro_placeholder() # Chama a função de simulação no AppState

    def restore_purchases_click(e):
        """Chamada ao clicar em 'Restaurar Compras'."""
        print("Simulando restauração de compras...")
        state.purchase_pro_placeholder() # Placeholder chama a mesma função por enquanto

    def deactivate_pro_click(e):
        """Chamada ao clicar em 'Desativar Pro'."""
        state.deactivate_pro_placeholder()


    # --- Funções de Importação/Exportação ---
    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                associations = get_all_player_list_associations()
                with open(e.path, "w", newline="", encoding="utf-8-sig") as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow(["player_id", "player_name", "player_skill", "player_photo_path", "list_name"])
                    writer.writerows(associations)
                state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "export_success")), bgcolor=ft.colors.GREEN_700) # Usa ft.colors.
            except Exception as ex:
                state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "export_error", error=ex)), bgcolor=ft.colors.RED_700) # Usa ft.colors.
            state.page.snack_bar.open = True; state.update()

    export_file_picker = ft.FilePicker(on_result=save_file_result)

    def export_data_click(e):
        # --- VERIFICAÇÃO PRO ---
        if not state.is_pro:
            state.page.show_dialog(ft.AlertDialog(
                 title=ft.Text(get_string(state, "feature_for_pro_title")),
                 content=ft.Text(get_string(state, "import_export_pro_feature_message")),
                 actions=[
                     ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.update()),
                     ft.ElevatedButton(get_string(state, "upgrade_button"), on_click=lambda _: state.navigate_to("settings")) # Leva para Configurações (onde já está)
                 ]
            ))
            state.update()
            return # Impede a exportação

        # Se for Pro, continua normal
        export_file_picker.save_file(
            dialog_title=get_string(state, "save_file_dialog_title"),
            file_name="listas_de_jogadores.csv",
            allowed_extensions=["csv"]
        )

    def perform_import(file_path, mode):
        # ... (lógica interna como antes, usa ft.colors.) ...
        added_players = 0; updated_players = 0; skipped_players = 0; added_lists = 0;
        try:
            with open(file_path, "r", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';'); lists_cache = {}; players_cache = {}
                for row in reader:
                    list_name = row.get("list_name"); player_name = row.get("player_name")
                    if not list_name or not player_name: continue
                    list_id = lists_cache.get(list_name)
                    if not list_id: existing_list = get_list_by_name(list_name); list_id = existing_list[0] if existing_list else create_list(list_name); added_lists += 1 if not existing_list else 0; lists_cache[list_name] = list_id
                    player_id = players_cache.get(player_name)
                    if not player_id:
                        existing_player = get_player_by_name(player_name)
                        if existing_player:
                            player_id = existing_player[0]
                            if mode == "overwrite": update_player(player_id, player_name, int(row.get("player_skill", 0)), row.get("player_photo_path")); updated_players += 1
                            else: skipped_players += 1
                        else: player_id = insert_player(player_name, int(row.get("player_skill", 0)), row.get("player_photo_path")); added_players += 1
                        players_cache[player_name] = player_id
                    if player_id and list_id: add_player_to_list(list_id, player_id)
            summary_message = get_string(state, "import_summary", added_players=added_players, added_lists=added_lists, updated_players=updated_players, skipped_players=skipped_players)
            state.page.snack_bar = ft.SnackBar(ft.Text(summary_message), bgcolor=ft.colors.GREEN_700, duration=4000) # Usa ft.colors.
        except Exception as ex: state.page.snack_bar = ft.SnackBar(ft.Text(get_string(state, "import_error", error=ex)), bgcolor=ft.colors.RED_700) # Usa ft.colors.
        if state.page.dialog: state.page.dialog.open = False
        state.page.snack_bar.open = True; state.update()

    def open_file_result(e: ft.FilePickerResultEvent):
        # ... (lógica interna como antes) ...
        if e.files:
            file_path = e.files[0].path
            import_mode_selection = ft.RadioGroup(content=ft.Row([ft.Radio(value="ignore", label=get_string(state, "import_mode_ignore")), ft.Radio(value="overwrite", label=get_string(state, "import_mode_overwrite"))]), value="ignore")
            def continue_import(e): perform_import(file_path, import_mode_selection.value)
            confirm_dialog = ft.AlertDialog(modal=True, title=ft.Text(get_string(state, "import_dialog_title")), content=ft.Column([ft.Text(get_string(state, "import_dialog_content")), import_mode_selection], tight=True, width=350), actions=[ft.TextButton(get_string(state, "cancel_button"), on_click=lambda e: setattr(confirm_dialog, 'open', False) or state.update()), ft.ElevatedButton(get_string(state, "continue_import_button"), on_click=continue_import)], actions_alignment=ft.MainAxisAlignment.END, shape=ft.RoundedRectangleBorder(radius=10),)
            state.page.dialog = confirm_dialog; confirm_dialog.open = True; state.update()

    import_file_picker = ft.FilePicker(on_result=open_file_result)
    if state.page: # Adiciona pickers à overlay
        current_overlay_controls = state.page.overlay[:]
        if export_file_picker not in current_overlay_controls: state.page.overlay.append(export_file_picker)
        if import_file_picker not in current_overlay_controls: state.page.overlay.append(import_file_picker)

    def import_data_click(e):
        # --- VERIFICAÇÃO PRO ---
        if not state.is_pro:
            state.page.show_dialog(ft.AlertDialog( title=ft.Text(get_string(state, "feature_for_pro_title")), content=ft.Text(get_string(state, "import_export_pro_feature_message")), actions=[ft.TextButton(get_string(state, "cancel_button"), on_click=lambda _: setattr(state.page.dialog, 'open', False) or state.update()), ft.ElevatedButton(get_string(state, "upgrade_button"), on_click=lambda _: state.navigate_to("settings"))] ))
            state.update(); return
        # Continua se for Pro
        import_file_picker.pick_files( dialog_title=get_string(state, "open_file_dialog_title"), allow_multiple=False, allowed_extensions=["csv"] )

    # --- MONTAGEM DA VIEW ---
    view = ft.Column(
        controls=[
            ft.Row([
                ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main"), tooltip=get_string(state, "back_button_tooltip")),
                ft.Text(get_string(state, "settings_title"), size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER),
                state.theme_toggle_button if state.theme_toggle_button else ft.Container(width=48) # Placeholder width
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(),
            ft.Container( content=ft.Row([language_dropdown]), padding=ft.padding.symmetric(horizontal=10) ),
            ft.Divider(),
            ft.ListView(
                expand=True,
                spacing=0,
                controls=[
                    # Opções Pro
                    ft.ListTile(
                        leading=ft.Icon(name="workspace_premium", color=ft.colors.AMBER_700 if not state.is_pro else ft.colors.GREEN_700), # Usa ft.colors.
                        title=ft.Text(get_string(state, "become_pro_title")),
                        subtitle=ft.Text(get_string(state, "become_pro_subtitle", status=(get_string(state, "status_pro") if state.is_pro else get_string(state, "status_free")))),
                        on_click=buy_pro_click,
                        disabled=state.is_pro
                    ),
                    ft.ListTile(
                        leading=ft.Icon(name="restore"),
                        title=ft.Text(get_string(state, "restore_purchases_title")),
                        subtitle=ft.Text(get_string(state, "restore_purchases_subtitle")),
                        on_click=restore_purchases_click,
                        disabled=state.is_pro
                    ),
                    # Botão Desativar Pro
                    ft.ListTile(
                        leading=ft.Icon(name="cancel", color=ft.colors.RED_700), # Usa ft.colors.
                        title=ft.Text(get_string(state, "deactivate_pro_title")),
                        subtitle=ft.Text(get_string(state, "deactivate_pro_subtitle")),
                        on_click=deactivate_pro_click,
                        visible=state.is_pro # Só mostra se FOR Pro
                    ),
                    ft.Divider(), # Movido para depois das opções Pro/Desativar

                    # Opções Import/Export
                    ft.ListTile(
                        leading=ft.Icon(name="upload_file"),
                        title=ft.Text(get_string(state, "export_title")),
                        subtitle=ft.Text(get_string(state, "export_subtitle")),
                        on_click=export_data_click # Chama função com verificação Pro
                    ),
                    ft.ListTile(
                        leading=ft.Icon(name="download"),
                        title=ft.Text(get_string(state, "import_title")),
                        subtitle=ft.Text(get_string(state, "import_subtitle")),
                        on_click=import_data_click # Chama função com verificação Pro
                    ),
                    # Links Legais
                    ft.Divider(),
                    ft.ListTile(
                        leading=ft.Icon(name="policy"),
                        title=ft.Text(get_string(state, "privacy_policy_link_title")),
                        on_click=lambda _: state.navigate_to("privacy_policy"),
                        trailing=ft.Icon(name="chevron_right")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(name="gavel"),
                        title=ft.Text(get_string(state, "terms_of_use_link_title")),
                        on_click=lambda _: state.navigate_to("terms_of_use"),
                        trailing=ft.Icon(name="chevron_right")
                    ),
                ]
            )
        ],
        expand=True # Garante que a coluna principal ocupe todo o espaço
    )
    return view