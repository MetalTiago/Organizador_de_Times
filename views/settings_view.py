# views/settings_view.py
import flet as ft
import csv
from db_handler import (
    get_all_player_list_associations, 
    get_player_by_name, 
    get_list_by_name,
    insert_player, 
    update_player,
    create_list,
    add_player_to_list
)
from localization import get_string # --- 1. IMPORTE A FUNÇÃO ---

def build_settings_view(state):
    """Constrói a view de Configurações."""

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                associations = get_all_player_list_associations()
                with open(e.path, "w", newline="", encoding="utf-8-sig") as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow(["player_id", "player_name", "player_skill", "player_photo_path", "list_name"])
                    writer.writerows(associations)
                state.page.snack_bar = ft.SnackBar(ft.Text(f"Listas e jogadores exportados com sucesso!"), bgcolor=ft.colors.GREEN_700)
            except Exception as ex:
                state.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao exportar arquivo: {ex}"), bgcolor=ft.colors.RED_700)
            state.page.snack_bar.open = True; state.update()

    export_file_picker = ft.FilePicker(on_result=save_file_result)

    def export_data_click(e):
        export_file_picker.save_file(dialog_title="Salvar Arquivo de Listas e Jogadores", file_name="listas_de_jogadores.csv", allowed_extensions=["csv"])

    def perform_import(file_path, mode):
        # (Lógica de importação permanece a mesma por enquanto)
        added_players = 0; updated_players = 0; skipped_players = 0
        added_lists = 0;
        
        try:
            with open(file_path, "r", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                
                lists_cache = {}
                players_cache = {}

                for row in reader:
                    list_name = row.get("list_name")
                    player_name = row.get("player_name")

                    if not list_name or not player_name:
                        continue
                    
                    list_id = lists_cache.get(list_name)
                    if not list_id:
                        existing_list = get_list_by_name(list_name)
                        if existing_list:
                            list_id = existing_list[0]
                        else:
                            list_id = create_list(list_name)
                            added_lists += 1
                        lists_cache[list_name] = list_id
                    
                    player_id = players_cache.get(player_name)
                    if not player_id:
                        existing_player = get_player_by_name(player_name)
                        if existing_player:
                            player_id = existing_player[0]
                            if mode == "overwrite":
                                update_player(player_id, player_name, int(row.get("player_skill", 0)), row.get("player_photo_path"))
                                updated_players += 1
                            else: # mode == "ignore"
                                skipped_players += 1
                        else:
                            player_id = insert_player(player_name, int(row.get("player_skill", 0)), row.get("player_photo_path"))
                            added_players += 1
                        players_cache[player_name] = player_id

                    if player_id and list_id:
                        add_player_to_list(list_id, player_id)

            summary_message = f"Importação: {added_players} jogadores e {added_lists} listas criados. {updated_players} jogadores atualizados, {skipped_players} ignorados."
            state.page.snack_bar = ft.SnackBar(ft.Text(summary_message), bgcolor=ft.colors.GREEN_700, duration=4000)

        except Exception as ex:
            state.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao importar arquivo: {ex}"), bgcolor=ft.colors.RED_700)
        
        state.page.dialog.open = False
        state.page.snack_bar.open = True
        state.update()

    def open_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            import_mode_selection = ft.RadioGroup(
                content=ft.Row([ft.Radio(value="ignore", label="Ignorar"), ft.Radio(value="overwrite", label="Sobrescrever")]), value="ignore"
            )
            def continue_import(e):
                perform_import(file_path, import_mode_selection.value)
            confirm_dialog = ft.AlertDialog(
                modal=True, title=ft.Text("Modo de Importação"),
                content=ft.Column([ft.Text("O que fazer com jogadores do arquivo que já existem no app?"), import_mode_selection], tight=True, width=350),
                actions=[ft.TextButton("Cancelar", on_click=lambda e: setattr(confirm_dialog, 'open', False) or state.update()), ft.ElevatedButton("Continuar Importação", on_click=continue_import)],
                actions_alignment=ft.MainAxisAlignment.END, shape=ft.RoundedRectangleBorder(radius=10),
            )
            state.page.dialog = confirm_dialog; confirm_dialog.open = True; state.update()

    import_file_picker = ft.FilePicker(on_result=open_file_result)
    state.page.overlay.clear()
    state.page.overlay.append(export_file_picker)
    state.page.overlay.append(import_file_picker)

    def import_data_click(e):
        import_file_picker.pick_files(dialog_title="Abrir Arquivo de Listas e Jogadores", allow_multiple=False, allowed_extensions=["csv"])

    view = ft.Column(
        controls=[
            # --- 2. SUBSTITUA OS TEXTOS FIXOS ---
            ft.Row([
                ft.IconButton(icon="arrow_back", on_click=lambda e: state.navigate_to("main"), tooltip=get_string(state, "back_button_tooltip")), 
                ft.Text(get_string(state, "settings_title"), size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER), 
                ft.Container(width=40)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(),
            ft.ListView(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.UPLOAD_FILE_SHARP), 
                        title=ft.Text(get_string(state, "export_title")), 
                        subtitle=ft.Text(get_string(state, "export_subtitle")), 
                        on_click=export_data_click
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.DOWNLOAD_SHARP), 
                        title=ft.Text(get_string(state, "import_title")), 
                        subtitle=ft.Text(get_string(state, "import_subtitle")), 
                        on_click=import_data_click
                    ),
                ]
            )
        ],
        expand=True
    )
    return view