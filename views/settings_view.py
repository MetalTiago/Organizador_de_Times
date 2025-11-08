# views/settings_view.py
import flet as ft
import csv
# import asyncio # <-- REMOVIDO
from db_handler import (
    get_all_player_list_associations, get_player_by_name, get_list_by_name,
    insert_player, update_player, create_list, add_player_to_list
)
from localization import get_string

def build_settings_view(state):
    """Constrói a view de Configurações."""

    def change_language(e):
        selected_lang_code = e.control.value
        if selected_lang_code != state.current_language:
            state.current_language = selected_lang_code 
            state.save_language_preference(selected_lang_code) 
            state.navigate_to("settings")
            if state.page:
                state.page.title = get_string(state, "app_title")
                state.page.update()

    language_dropdown = ft.Dropdown(
        label=get_string(state, "language_selection_label"),
        value=state.current_language, 
        options=[
            ft.dropdown.Option("pt_br", get_string(state, "language_pt_br")),
            ft.dropdown.Option("en_us", get_string(state, "language_en_us")),
            ft.dropdown.Option("es", get_string(state, "language_es")),
        ],
        on_change=change_language,
        expand=True
    )

    # --- Funções Pro REMOVIDAS ---

    def save_file_result(e: ft.FilePickerResultEvent): # <--- Revertido para 'def'
        if e.path:
            try:
                associations = get_all_player_list_associations()
                with open(e.path, "w", newline="", encoding="utf-8-sig") as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow(["player_id", "player_name", "player_skill", "player_photo_path", "list_name"])
                    writer.writerows(associations)
                state.page.snack_bar = ft.SnackBar(
                    ft.Text(get_string(state, "export_success")), 
                    bgcolor="green_700"
                )
                state.page.snack_bar.open = True
            except Exception as ex:
                state.page.snack_bar = ft.SnackBar(
                    ft.Text(get_string(state, "export_error", error=ex)), 
                    bgcolor="red_700"
                )
                state.page.snack_bar.open = True
            state.page.update() # <--- update() síncrono

    if state.export_file_picker:
        state.export_file_picker.on_result = save_file_result # <--- Revertido

    def export_data_click(e): # <--- Revertido para 'def'
        if state.export_file_picker:
            state.export_file_picker.save_file( # <--- Revertido para 'save_file'
                dialog_title=get_string(state, "save_file_dialog_title"),
                file_name="listas_de_jogadores.csv",
                allowed_extensions=["csv"]
            )
        else:
            print("Export file picker não inicializado")

    def perform_import(file_path, mode, dialog_to_close): # <--- Revertido para 'def'
        added_players = 0; updated_players = 0; skipped_players = 0; added_lists = 0;
        snack_bar = None
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
            snack_bar = ft.SnackBar(
                ft.Text(summary_message), 
                bgcolor="green_700", 
                duration=4000
            )
        except Exception as ex: 
            snack_bar = ft.SnackBar(
                ft.Text(get_string(state, "import_error", error=ex)), 
                bgcolor="red_700"
            )
        
        state.page.close(dialog_to_close)
        
        if snack_bar:
            state.page.snack_bar = snack_bar
            snack_bar.open = True
            state.page.update() # <--- update() síncrono
        else:
            state.page.update() # <--- update() síncrono

    def open_file_result(e: ft.FilePickerResultEvent): # <--- Revertido para 'def'
        if e.files:
            file_path = e.files[0].path
            import_mode_selection = ft.RadioGroup(content=ft.Row([ft.Radio(value="ignore", label=get_string(state, "import_mode_ignore")), ft.Radio(value="overwrite", label=get_string(state, "import_mode_overwrite"))]), value="ignore")
            
            confirm_dialog = ft.AlertDialog(
                modal=True, 
                title=ft.Text(get_string(state, "import_dialog_title")), 
                content=ft.Column([
                    ft.Text(get_string(state, "import_dialog_content")), 
                    import_mode_selection
                ], tight=True, width=350), 
                actions_alignment=ft.MainAxisAlignment.END, 
                shape=ft.RoundedRectangleBorder(radius=10)
            )

            def continue_import(e): # <--- Revertido para 'def'
                perform_import(file_path, import_mode_selection.value, confirm_dialog)

            confirm_dialog.actions = [
                ft.TextButton(get_string(state, "cancel_button"), on_click=lambda e: state.page.close(confirm_dialog)), 
                ft.ElevatedButton(get_string(state, "continue_import_button"), on_click=continue_import) # <--- Revertido
            ]
            
            state.page.open(confirm_dialog)

    if state.import_file_picker:
        state.import_file_picker.on_result = open_file_result # <--- Revertido

    def import_data_click(e): # <--- Revertido para 'def'
        if state.import_file_picker:
            state.import_file_picker.pick_files( # <--- Revertido para 'pick_files'
                dialog_title=get_string(state, "open_file_dialog_title"), 
                allow_multiple=False, allowed_extensions=["csv"] 
            )
        else:
            print("Import file picker não inicializado")

    view = ft.Column(
        controls=[
            ft.Row([
                ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main"), tooltip=get_string(state, "back_button_tooltip")),
                ft.Text(get_string(state, "settings_title"), size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER),
                state.theme_toggle_button if state.theme_toggle_button else ft.Container(width=48) 
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(),
            ft.Container( content=ft.Row([language_dropdown]), padding=ft.padding.symmetric(horizontal=10) ),
            ft.Divider(),
            ft.ListView(
                expand=True,
                spacing=0,
                controls=[
                    # --- Opções Pro REMOVIDAS ---
                    
                    # Opções Import/Export
                    ft.ListTile(
                        leading=ft.Icon(name="upload_file"),
                        title=ft.Text(get_string(state, "export_title")),
                        subtitle=ft.Text(get_string(state, "export_subtitle")),
                        on_click=export_data_click # <--- Revertido
                    ),
                    ft.ListTile(
                        leading=ft.Icon(name="download"),
                        title=ft.Text(get_string(state, "import_title")),
                        subtitle=ft.Text(get_string(state, "import_subtitle")),
                        on_click=import_data_click # <--- Revertido
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
        expand=True 
    )
    return view
