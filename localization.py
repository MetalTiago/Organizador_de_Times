# localization.py

# Dicionário para nomes de cores, para serem usados na tela de resultados
TEAM_COLORS = {
    "pt_br": ["Vermelho", "Azul", "Verde", "Amarelo", "Roxo", "Laranja", "Ciano", "Rosa", "Verde Limão", "Índigo"],
    "en_us": ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Cyan", "Pink", "Lime Green", "Indigo"],
    "es": ["Rojo", "Azul", "Verde", "Amarillo", "Morado", "Naranja", "Cian", "Rosa", "Verde Lima", "Índigo"],
}

STRINGS = {
    "pt_br": {
        # Main View & Menus
        "app_title": "Organizador de Times",
        "toggle_theme_tooltip": "Alternar Tema", # Corrigido/Adicionado
        "settings_tooltip": "Configurações",
        "select_list_label": "Selecione a Lista:",
        "organize_button_text": "Organizar Times",
        "organize_button_tooltip_disabled": "Selecione uma lista específica para poder organizar os times",
        "register_player_button_text": "Cadastrar Jogador",
        "filter_by_name_label": "Filtrar por Nome...",
        "all_players_list_name": "Jogadores Cadastrados",
        "create_new_list_menu": "Criar nova lista",
        "rename_list_menu": "Renomear lista atual",
        "manage_players_menu": "Gerenciar Jogadores",
        "delete_list_menu": "Excluir lista atual",

        "# Language Selection": "",
        "language_selection_label": "Idioma do Aplicativo:",
        "language_pt_br": "Português (Brasil)",
        "language_en_us": "Inglês (EUA)",
        "language_es": "Espanhol",

        "export_success": "Listas e jogadores exportados com sucesso!",
        "export_error": "Erro ao exportar arquivo: {error}",
        "import_summary": "Importação: {added_players} jogadores e {added_lists} listas criados. {updated_players} jogadores atualizados, {skipped_players} ignorados.",
        "import_error": "Erro ao importar arquivo: {error}",

        # Components (Formulários & Diálogos)
        "player_name_label": "Nome",
        "name_cannot_be_empty_error": "O nome não pode estar vazio",
        "select_at_least_one_list_error": "Selecione pelo menos uma lista!",
        "player_saved_success": "Cadastrado com sucesso",
        "player_updated_success": "Jogador atualizado!",
        "generic_error": "Erro ao cadastrar: {error}",
        "new_player_title": "Novo Jogador",
        "edit_player_title": "Editar Jogador",
        "choose_photo_button": "Escolher Foto",
        "change_photo_button": "Mudar Foto",
        "skill_label": "Skill:",
        "add_to_lists_label": "Adicionar às Listas:",
        "save_player_button": "Salvar Jogador",
        "update_button": "Atualizar",
        "delete_confirmation_title": "Confirmação de Exclusão", # Adicionado
        "delete_player_confirmation_content": "Tem certeza que deseja excluir este jogador?", # Adicionado
        "delete_list_confirmation_content": "Tem certeza que deseja apagar a lista '{list_name}'?", # Adicionado
        "yes_button": "Sim", # Adicionado
        "no_button": "Não", # Adicionado
        "cancel_button": "Cancelar", # Adicionado
        "save_button": "Salvar", # Adicionado
        "player_deleted_success": "Jogador excluído!", # Adicionado
        "edit_tooltip": "Editar", # Adicionado
        "delete_tooltip": "Excluir", # Adicionado
        "empty_state_title": "Nenhum jogador por aqui...",
        "empty_state_subtitle1": "Clique em 'Cadastrar Jogador' para adicionar o primeiro!",
        "empty_state_subtitle2": "Ou use o menu (⋮) e 'Gerenciar Jogadores' para adicionar jogadores já existentes a esta lista.",

        # Dialogs
        "create_list_dialog_title": "Criar Nova Lista", # Adicionado
        "new_list_name_label": "Nome da Nova Lista", # Adicionado
        "list_already_exists_error": "Esta lista já existe.", # Adicionado
        "rename_list_dialog_title": "Renomear Lista", # Adicionado
        "new_list_name_label_edit": "Novo nome da lista", # Adicionado
        "list_renamed_success": "Lista renomeada com sucesso!", # Adicionado
        "cannot_delete_last_list_error": "Não é possível apagar a última lista.", # Adicionado

        # Settings View
        "settings_title": "Configurações",
        "back_button_tooltip": "Voltar",
        "export_title": "Exportar Listas e Jogadores",
        "export_subtitle": "Salva listas e jogadores em um arquivo CSV.",
        "import_title": "Importar Listas e Jogadores",
        "import_subtitle": "Adiciona listas e jogadores de um arquivo CSV.",
        "save_file_dialog_title": "Salvar Arquivo de Listas e Jogadores", # Adicionado
        "open_file_dialog_title": "Abrir Arquivo de Listas e Jogadores", # Adicionado
        "import_dialog_title": "Modo de Importação", # Adicionado
        "import_dialog_content": "O que fazer com jogadores do arquivo que já existem no app?", # Adicionado
        "import_mode_ignore": "Ignorar", # Adicionado
        "import_mode_overwrite": "Sobrescrever", # Adicionado
        "continue_import_button": "Continuar Importação", # Adicionado

        # Selection View
        "selection_title": "Selecionar Jogadores",
        "selected_players_count": "Jogadores selecionados: {count}",
        "clear_button": "Limpar",
        "teams_count": "{count} Times",

        # Results View
        "results_title": "Times Gerados",
        "reorganize_button": "Reorganizar",
        "share_all_button": "Compartilhar Todos",
        "reorganizing_dialog_title": "Reorganizando...",
        "organizing_dialog_title": "Organizando...",
        "generate_teams_first_error": "Gere os times primeiro!",
        "all_teams_copied_success": "Times copiados!",
        "team_copied_success": "{team_name} copiado!",
        "total_skill_label": "Total Skill:", # Corrigido/Adicionado
        "copy_button_tooltip": "Copiar {team_name}",
        "team_name_prefix": "Time {color_name}", # Usaremos com get_team_color_name
    },
    "en_us": {
        # Main View & Menus
        "app_title": "Team Organizer",
        "toggle_theme_tooltip": "Toggle Theme", # Corrigido/Adicionado
        "settings_tooltip": "Settings",
        "select_list_label": "Select a List:",
        "organize_button_text": "Organize Teams",
        "organize_button_tooltip_disabled": "Select a specific list to organize teams",
        "register_player_button_text": "Register Player",
        "filter_by_name_label": "Filter by Name...",
        "all_players_list_name": "All Registered Players",
        "create_new_list_menu": "Create new list",
        "rename_list_menu": "Rename current list",
        "manage_players_menu": "Manage Players",
        "delete_list_menu": "Delete current list",

        "# Language Selection": "",
        "language_selection_label": "App Language:",
        "language_pt_br": "Portuguese (Brazil)",
        "language_en_us": "English (US)",
        "language_es": "Spanish",

        "export_success": "Lists and players exported successfully!",
        "export_error": "Error exporting file: {error}",
        "import_summary": "Import: {added_players} players and {added_lists} lists created. {updated_players} players updated, {skipped_players} skipped.",
        "import_error": "Error importing file: {error}",

        # Components (Forms & Dialogs)
        "player_name_label": "Name",
        "name_cannot_be_empty_error": "Name cannot be empty",
        "select_at_least_one_list_error": "Select at least one list!",
        "player_saved_success": "Registered successfully",
        "player_updated_success": "Player updated!",
        "generic_error": "Error while saving: {error}",
        "new_player_title": "New Player",
        "edit_player_title": "Edit Player",
        "choose_photo_button": "Choose Photo",
        "change_photo_button": "Change Photo",
        "skill_label": "Skill:",
        "add_to_lists_label": "Add to Lists:",
        "save_player_button": "Save Player",
        "update_button": "Update",
        "delete_confirmation_title": "Delete Confirmation", # Adicionado
        "delete_player_confirmation_content": "Are you sure you want to delete this player?", # Adicionado
        "delete_list_confirmation_content": "Are you sure you want to delete the list '{list_name}'?", # Adicionado
        "yes_button": "Yes", # Adicionado
        "no_button": "No", # Adicionado
        "cancel_button": "Cancel", # Adicionado
        "save_button": "Save", # Adicionado
        "player_deleted_success": "Player deleted!", # Adicionado
        "edit_tooltip": "Edit", # Adicionado
        "delete_tooltip": "Delete", # Adicionado
        "empty_state_title": "No players around here...",
        "empty_state_subtitle1": "Click 'Register Player' to add the first one!",
        "empty_state_subtitle2": "Or use the (⋮) menu and 'Manage Players' to add existing players to this list.",

        # Dialogs
        "create_list_dialog_title": "Create New List", # Adicionado
        "new_list_name_label": "New List Name", # Adicionado
        "list_already_exists_error": "This list already exists.", # Adicionado
        "rename_list_dialog_title": "Rename List", # Adicionado
        "new_list_name_label_edit": "New list name", # Adicionado
        "list_renamed_success": "List renamed successfully!", # Adicionado
        "cannot_delete_last_list_error": "Cannot delete the last list.", # Adicionado
        
        # Settings View
        "settings_title": "Settings",
        "back_button_tooltip": "Back",
        "export_title": "Export Lists and Players",
        "export_subtitle": "Saves lists and players to a CSV file.",
        "import_title": "Import Lists and Players",
        "import_subtitle": "Adds lists and players from a CSV file.",
        "save_file_dialog_title": "Save Lists and Players File", # Adicionado
        "open_file_dialog_title": "Open Lists and Players File", # Adicionado
        "import_dialog_title": "Import Mode", # Adicionado
        "import_dialog_content": "What to do with players from the file that already exist in the app?", # Adicionado
        "import_mode_ignore": "Ignore", # Adicionado
        "import_mode_overwrite": "Overwrite", # Adicionado
        "continue_import_button": "Continue Import", # Adicionado

        # Selection View
        "selection_title": "Select Players",
        "selected_players_count": "Players selected: {count}",
        "clear_button": "Clear",
        "teams_count": "{count} Teams",

        # Results View
        "results_title": "Generated Teams",
        "reorganize_button": "Reorganize",
        "share_all_button": "Share All",
        "reorganizing_dialog_title": "Reorganizing...",
        "organizing_dialog_title": "Organizing...",
        "generate_teams_first_error": "Generate the teams first!",
        "all_teams_copied_success": "Teams copied!",
        "team_copied_success": "{team_name} copied!",
        "total_skill_label": "Total Skill:", # Corrigido/Adicionado
        "copy_button_tooltip": "Copy {team_name}",
        "team_name_prefix": "Team {color_name}", # Usaremos com get_team_color_name

        # Manage Players View
        "manage_list_title": "Managing List:",
        "rename_list_tooltip": "Rename List",
        "save_changes_button": "Save Changes",
        "list_updated_success": "List updated successfully!",
        "save_error": "Error while saving: {error}",
    },
    "es": {
        # Main View & Menus
        "app_title": "Organizador de Equipos",
        "toggle_theme_tooltip": "Cambiar Tema", # Corrigido/Adicionado
        "settings_tooltip": "Configuración",
        "select_list_label": "Selecciona la Lista:",
        "organize_button_text": "Organizar Equipos",
        "organize_button_tooltip_disabled": "Selecciona una lista específica para organizar equipos",
        "register_player_button_text": "Registrar Jugador",
        "filter_by_name_label": "Filtrar por Nombre...",
        "all_players_list_name": "Todos los Jugadores",
        "create_new_list_menu": "Crear nueva lista",
        "rename_list_menu": "Renombrar lista actual",
        "manage_players_menu": "Gestionar Jugadores",
        "delete_list_menu": "Eliminar lista actual",

        "# Language Selection": "",
        "language_selection_label": "Idioma de la Aplicación:",
        "language_pt_br": "Portugués (Brasil)",
        "language_en_us": "Inglés (EE.UU.)",
        "language_es": "Español",

        "export_success": "¡Listas y jugadores exportados con éxito!",
        "export_error": "Error al exportar archivo: {error}",
        "import_summary": "Importación: {added_players} jugadores y {added_lists} listas creados. {updated_players} jugadores actualizados, {skipped_players} ignorados.",
        "import_error": "Error al importar archivo: {error}",

        # Components (Forms & Dialogs)
        "player_name_label": "Nombre",
        "name_cannot_be_empty_error": "El nombre no puede estar vacío",
        "select_at_least_one_list_error": "¡Selecciona al menos una lista!",
        "player_saved_success": "Registrado con éxito",
        "player_updated_success": "¡Jugador actualizado!",
        "generic_error": "Error al registrar: {error}",
        "new_player_title": "Nuevo Jugador",
        "edit_player_title": "Editar Jugador",
        "choose_photo_button": "Elegir Foto",
        "change_photo_button": "Cambiar Foto",
        "skill_label": "Habilidad:",
        "add_to_lists_label": "Añadir a Listas:",
        "save_player_button": "Guardar Jugador",
        "update_button": "Actualizar",
        "delete_confirmation_title": "Confirmar Eliminación", # Adicionado
        "delete_player_confirmation_content": "¿Estás seguro de que quieres eliminar a este jugador?", # Adicionado
        "delete_list_confirmation_content": "¿Estás seguro de que quieres borrar la lista '{list_name}'?", # Adicionado
        "yes_button": "Sí", # Adicionado
        "no_button": "No", # Adicionado
        "cancel_button": "Cancelar", # Adicionado
        "save_button": "Guardar", # Adicionado
        "player_deleted_success": "¡Jugador eliminado!", # Adicionado
        "edit_tooltip": "Editar", # Adicionado
        "delete_tooltip": "Eliminar", # Adicionado
        "empty_state_title": "No hay jugadores por aquí...",
        "empty_state_subtitle1": "¡Haz clic en 'Registrar Jugador' para añadir el primero!",
        "empty_state_subtitle2": "O usa el menú (⋮) y 'Gestionar Jugadores' para añadir jugadores existentes a esta lista.",

        # Dialogs
        "create_list_dialog_title": "Crear Nueva Lista", # Adicionado
        "new_list_name_label": "Nombre de la Nueva Lista", # Adicionado
        "list_already_exists_error": "Esta lista ya existe.", # Adicionado
        "rename_list_dialog_title": "Renombrar Lista", # Adicionado
        "new_list_name_label_edit": "Nuevo nombre de la lista", # Adicionado
        "list_renamed_success": "¡Lista renombrada con éxito!", # Adicionado
        "cannot_delete_last_list_error": "No se puede borrar la última lista.", # Adicionado
        
        # Settings View
        "settings_title": "Configuración",
        "back_button_tooltip": "Volver",
        "export_title": "Exportar Listas y Jugadores",
        "export_subtitle": "Guarda listas y jugadores en un archivo CSV.",
        "import_title": "Importar Listas y Jugadores",
        "import_subtitle": "Añade listas y jugadores desde un archivo CSV.",
        "save_file_dialog_title": "Guardar Archivo de Listas y Jugadores", # Adicionado
        "open_file_dialog_title": "Abrir Archivo de Listas y Jugadores", # Adicionado
        "import_dialog_title": "Modo de Importación", # Adicionado
        "import_dialog_content": "¿Qué hacer con los jugadores del archivo que ya existen en la aplicación?", # Adicionado
        "import_mode_ignore": "Ignorar", # Adicionado
        "import_mode_overwrite": "Sobrescribir", # Adicionado
        "continue_import_button": "Continuar Importación", # Adicionado
        
        # Selection View
        "selection_title": "Seleccionar Jugadores",
        "selected_players_count": "Jugadores seleccionados: {count}",
        "clear_button": "Limpiar",
        "teams_count": "{count} Equipos",

        # Results View
        "results_title": "Equipos Generados",
        "reorganize_button": "Reorganizar",
        "share_all_button": "Compartir Todos",
        "reorganizing_dialog_title": "Reorganizando...",
        "organizing_dialog_title": "Organizando...",
        "generate_teams_first_error": "¡Genera los equipos primero!",
        "all_teams_copied_success": "¡Equipos copiados!",
        "team_copied_success": "¡Equipo {team_name} copiado!",
        "total_skill_label": "Habilidad Total:", # Corrigido/Adicionado
        "copy_button_tooltip": "Copiar {team_name}",
        "team_name_prefix": "Equipo {color_name}", # Usaremos com get_team_color_name

        # Manage Players View
        "manage_list_title": "Gestionando la Lista:",
        "rename_list_tooltip": "Renombrar Lista",
        "save_changes_button": "Guardar Cambios",
        "list_updated_success": "¡Lista actualizada con éxito!",
        "save_error": "Error al guardar: {error}",
    }
}

def get_string(state, key, **kwargs):
    """Retorna a string traduzida com base no idioma atual do estado."""
    language_dict = STRINGS.get(state.current_language, STRINGS["en_us"])
    base_string = language_dict.get(key, STRINGS["en_us"].get(key, f"_{key}_"))
    return base_string.format(**kwargs)

def get_team_color_name(state, index):
    """Retorna o nome da cor do time no idioma atual."""
    color_names = TEAM_COLORS.get(state.current_language, TEAM_COLORS["en_us"])
    # Pega a cor correta, fazendo o índice "dar a volta" se necessário
    return color_names[index % len(color_names)]