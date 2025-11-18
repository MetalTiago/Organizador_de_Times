# localization.py
from collections import defaultdict

TEAM_COLORS = {
    "pt_br": ["Vermelho", "Azul", "Verde", "Amarelo", "Roxo", "Laranja", "Ciano", "Rosa", "Verde Limão", "Índigo"],
    "en_us": ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Cyan", "Pink", "Lime Green", "Indigo"],
    "es": ["Rojo", "Azul", "Verde", "Amarillo", "Morado", "Naranja", "Cian", "Rosa", "Verde Lima", "Índigo"],
}

STRINGS = {
    "pt_br": {
        # Geral
        "app_title": "Organizador de Times",
        "ok_button": "OK", # Adicionado para a SnackBar
        "welcome_message": "Bem-vindo ao Organizador de Times!", # Adicionado
        
        # Main View & Menus
        "toggle_theme_tooltip": "Alternar Tema", "settings_tooltip": "Configurações", "select_list_label": "Selecione a Lista:", "organize_button_text": "Organizar Times", "organize_button_tooltip_disabled": "Selecione uma lista específica para poder organizar os times", "register_player_button_text": "Cadastrar Jogador", "filter_by_name_label": "Filtrar por Nome...", "all_players_list_name": "Jogadores Cadastrados", "create_new_list_menu": "Criar nova lista", "rename_list_menu": "Renomear lista atual", "manage_players_menu": "Gerenciar Jogadores", "delete_list_menu": "Excluir lista atual",
        
        # Components (Formulários & Diálogos)
        "player_name_label": "Nome", "name_cannot_be_empty_error": "O nome não pode estar vazio", "select_at_least_one_list_error": "Selecione pelo menos uma lista!", "player_saved_success": "Jogador cadastrado com sucesso!", "player_updated_success": "Jogador atualizado com sucesso!", "generic_error": "Erro ao salvar: {error}", "new_player_title": "Novo Jogador", "edit_player_title": "Editar Jogador", "choose_photo_button": "Escolher Foto", "change_photo_button": "Mudar Foto", "skill_label": "Skill:", "add_to_lists_label": "Adicionar às Listas:", "save_player_button": "Salvar Jogador", "update_button": "Atualizar", "delete_confirmation_title": "Confirmação de Exclusão", "delete_player_confirmation_content": "Tem certeza que deseja excluir este jogador?", "delete_list_confirmation_content": "Tem certeza que deseja apagar a lista '{list_name}'?", "yes_button": "Sim", "no_button": "Não", "cancel_button": "Cancelar", "save_button": "Salvar", "player_deleted_success": "Jogador excluído com sucesso!", "edit_tooltip": "Editar", "delete_tooltip": "Excluir", "empty_state_title": "Nenhum jogador por aqui...", "empty_state_subtitle1": "Clique em 'Cadastrar Jogador' para adicionar o primeiro!", "empty_state_subtitle2": "Ou use o menu (⋮) e 'Gerenciar Jogadores' para adicionar jogadores já existentes a esta lista.",
        "list_created_success": "Lista '{list_name}' criada com sucesso!", # Adicionado
        "list_deleted_success": "Lista '{list_name}' excluída com sucesso.", # Adicionado

        # Dialogs
        "create_list_dialog_title": "Criar Nova Lista", "new_list_name_label": "Nome da Nova Lista", "list_already_exists_error": "Uma lista com este nome já existe.", "rename_list_dialog_title": "Renomear Lista", "new_list_name_label_edit": "Novo nome da lista", "list_renamed_success": "Lista renomeada com sucesso!", "cannot_delete_last_list_error": "Não é possível apagar a última lista.",
        
        # Settings View
        "settings_title": "Configurações", "back_button_tooltip": "Voltar", "export_title": "Exportar Listas e Jogadores", "export_subtitle": "Salva listas e jogadores em um arquivo CSV.", "import_title": "Importar Listas e Jogadores", "import_subtitle": "Adiciona listas e jogadores de um arquivo CSV.", "save_file_dialog_title": "Salvar Arquivo de Listas e Jogadores", "open_file_dialog_title": "Abrir Arquivo de Listas e Jogadores", "import_dialog_title": "Modo de Importação", "import_dialog_content": "O que fazer com jogadores do arquivo que já existem no app?", "import_mode_ignore": "Ignorar", "import_mode_overwrite": "Sobrescrever", "continue_import_button": "Continuar Importação", "export_success": "Listas e jogadores exportados com sucesso!", "export_error": "Erro ao exportar arquivo: {error}", "import_summary": "Importação: {added_players} jogadores e {added_lists} listas criados. {updated_players} jogadores atualizados, {skipped_players} ignorados.", "import_error": "Erro ao importar arquivo: {error}", "language_selection_label": "Idioma do Aplicativo:", "language_pt_br": "Português (Brasil)", "language_en_us": "Inglês (EUA)", "language_es": "Espanhol",
      
        # Legal Screens Links (Settings View)
        "privacy_policy_link_title": "Política de Privacidade",
        "terms_of_use_link_title": "Termos de Uso",
        
        # Legal Screens Titles & Content
        "privacy_policy_title": "Política de Privacidade",
        "terms_of_use_title": "Termos de Uso",
        
        # Selection View
        "selection_title": "Selecionar Jogadores", "selected_players_count": "Jogadores selecionados: {count}", "clear_button": "Limpar", "teams_count": "{count} Times", "selection_error": "Verifique o nº de times e jogadores.",
        
        # Results View
        "results_title": "Times Gerados", "reorganize_button": "Reorganizar", "share_all_button": "Compartilhar Todos", "reorganizing_dialog_title": "Reorganizando...", "organizing_dialog_title": "Organizando...", "generate_teams_first_error": "Gere os times primeiro!", "all_teams_copied_success": "Todos os times copiados!", "team_copied_success": "{team_name} copiado!", "total_skill_label": "Total Skill:", "copy_button_tooltip": "Copiar {team_name}", "team_name_prefix": "Time {color_name}",
        
        # Manage Players View
        "manage_list_title": "Gerenciando a Lista:", "rename_list_tooltip": "Renomear Lista", "save_changes_button": "Salvar Alterações", "list_updated_success": "Lista atualizada com sucesso!", "save_error": "Erro ao salvar: {error}",
    },
    "en_us": {
        # Geral
        "app_title": "Team Organizer",
        "ok_button": "OK",
        "welcome_message": "Welcome to the Team Organizer!",
        
        # Main View & Menus
        "toggle_theme_tooltip": "Toggle Theme", "settings_tooltip": "Settings", "select_list_label": "Select a List:", "organize_button_text": "Organize Teams", "organize_button_tooltip_disabled": "Select a specific list to organize teams", "register_player_button_text": "Register Player", "filter_by_name_label": "Filter by Name...", "all_players_list_name": "All Registered Players", "create_new_list_menu": "Create new list", "rename_list_menu": "Rename current list", "manage_players_menu": "Manage Players", "delete_list_menu": "Delete current list",
        
        # Components (Formulários & Diálogos)
        "player_name_label": "Name", "name_cannot_be_empty_error": "Name cannot be empty", "select_at_least_one_list_error": "Select at least one list!", "player_saved_success": "Player registered successfully!", "player_updated_success": "Player updated successfully!", "generic_error": "Error while saving: {error}", "new_player_title": "New Player", "edit_player_title": "Edit Player", "choose_photo_button": "Choose Photo", "change_photo_button": "Change Photo", "skill_label": "Skill:", "add_to_lists_label": "Add to Lists:", "save_player_button": "Save Player", "update_button": "Update", "delete_confirmation_title": "Delete Confirmation", "delete_player_confirmation_content": "Are you sure you want to delete this player?", "delete_list_confirmation_content": "Are you sure you want to delete the list '{list_name}'?", "yes_button": "Yes", "no_button": "No", "cancel_button": "Cancel", "save_button": "Save", "player_deleted_success": "Player deleted successfully!", "edit_tooltip": "Edit", "delete_tooltip": "Delete", "empty_state_title": "No players around here...", "empty_state_subtitle1": "Click 'Register Player' to add the first one!", "empty_state_subtitle2": "Or use the (⋮) menu and 'Manage Players' to add existing players to this list.",
        "list_created_success": "List '{list_name}' created successfully!",
        "list_deleted_success": "List '{list_name}' deleted successfully.",

        # Dialogs
        "create_list_dialog_title": "Create New List", "new_list_name_label": "New List Name", "list_already_exists_error": "A list with this name already exists.", "rename_list_dialog_title": "Rename List", "new_list_name_label_edit": "New list name", "list_renamed_success": "List renamed successfully!", "cannot_delete_last_list_error": "Cannot delete the last list.",
        
        # Settings View
        "settings_title": "Settings", "back_button_tooltip": "Back", "export_title": "Export Lists and Players", "export_subtitle": "Saves lists and players to a CSV file.", "import_title": "Import Lists and Players", "import_subtitle": "Adds lists and players from a CSV file.", "save_file_dialog_title": "Save Lists and Players File", "open_file_dialog_title": "Open Lists and Players File", "import_dialog_title": "Import Mode", "import_dialog_content": "What to do with players from the file that already exist in the app?", "import_mode_ignore": "Ignore", "import_mode_overwrite": "Overwrite", "continue_import_button": "Continue Import", "export_success": "Lists and players exported successfully!", "export_error": "Error exporting file: {error}", "import_summary": "Import: {added_players} players and {added_lists} lists created. {updated_players} players updated, {skipped_players} skipped.", "import_error": "Error importing file: {error}", "language_selection_label": "App Language:", "language_pt_br": "Portuguese (Brazil)", "language_en_us": "English (US)", "language_es": "Spanish",
       
        # Legal Screens Links (Settings View)
        "privacy_policy_link_title": "Privacy Policy",
        "terms_of_use_link_title": "Terms of Use",
        
        # Legal Screens Titles & Content
        "privacy_policy_title": "Privacy Policy",
        "terms_of_use_title": "Terms of Use",
        
        # Selection View
        "selection_title": "Select Players", "selected_players_count": "Players selected: {count}", "clear_button": "Clear", "teams_count": "{count} Teams", "selection_error": "Check team/player numbers.",

        # Results View
        "results_title": "Generated Teams", "reorganize_button": "Reorganize", "share_all_button": "Share All", "reorganizing_dialog_title": "Reorganizing...", "organizing_dialog_title": "Organizing...", "generate_teams_first_error": "Generate the teams first!", "all_teams_copied_success": "All teams copied!", "team_copied_success": "{team_name} copied!", "total_skill_label": "Total Skill:", "copy_button_tooltip": "Copy {team_name}", "team_name_prefix": "Team {color_name}",
        
        # Manage Players View
        "manage_list_title": "Managing List:", "rename_list_tooltip": "Rename List", "save_changes_button": "Save Changes", "list_updated_success": "List updated successfully!", "save_error": "Error while saving: {error}",
    },
    "es": {
        # Geral
        "app_title": "Organizador de Equipos",
        "ok_button": "OK",
        "welcome_message": "¡Bienvenido al Organizador de Equipos!",
        
        # Main View & Menus
        "toggle_theme_tooltip": "Cambiar Tema", "settings_tooltip": "Configuración", "select_list_label": "Selecciona la Lista:", "organize_button_text": "Organizar Equipos", "organize_button_tooltip_disabled": "Selecciona una lista específica para organizar equipos", "register_player_button_text": "Registrar Jugador", "filter_by_name_label": "Filtrar por Nombre...", "all_players_list_name": "Todos los Jugadores", "create_new_list_menu": "Crear nueva lista", "rename_list_menu": "Renombrar lista actual", "manage_players_menu": "Gestionar Jugadores", "delete_list_menu": "Eliminar lista actual",
        
        # Components (Formulários & Diálogos)
        "player_name_label": "Nombre", "name_cannot_be_empty_error": "El nombre no puede estar vacío", "select_at_least_one_list_error": "¡Selecciona al menos una lista!", "player_saved_success": "¡Jugador registrado con éxito!", "player_updated_success": "¡Jugador actualizado con éxito!", "generic_error": "Error al registrar: {error}", "new_player_title": "Nuevo Jugador", "edit_player_title": "Editar Jugador", "choose_photo_button": "Elegir Foto", "change_photo_button": "Cambiar Foto", "skill_label": "Habilidad:", "add_to_lists_label": "Añadir a Listas:", "save_player_button": "Guardar Jugador", "update_button": "Actualizar", "delete_confirmation_title": "Confirmar Eliminación", "delete_player_confirmation_content": "¿Estás seguro de que quieres eliminar a este jugador?", "delete_list_confirmation_content": "¿Estás seguro de que quieres borrar la lista '{list_name}'?", "yes_button": "Sí", "no_button": "No", "cancel_button": "Cancelar", "save_button": "Guardar", "player_deleted_success": "¡Jugador eliminado con éxito!", "edit_tooltip": "Editar", "delete_tooltip": "Eliminar", "empty_state_title": "No hay jugadores por aquí...", "empty_state_subtitle1": "¡Haz clic en 'Registrar Jugador' para añadir el primero!", "empty_state_subtitle2": "O usa el menú (⋮) y 'Gestionar Jugadores' para añadir jugadores existentes a esta lista.",
        "list_created_success": "¡Lista '{list_name}' creada con éxito!",
        "list_deleted_success": "Lista '{list_name}' eliminada con éxito.",

        # Dialogs
        "create_list_dialog_title": "Crear Nueva Lista", "new_list_name_label": "Nombre de la Nueva Lista", "list_already_exists_error": "Ya existe una lista con este nombre.", "rename_list_dialog_title": "Renombrar Lista", "new_list_name_label_edit": "Nuevo nombre de la lista", "list_renamed_success": "¡Lista renombrada con éxito!", "cannot_delete_last_list_error": "No se puede borrar la última lista.",
        
        # Settings View
        "settings_title": "Configuración", "back_button_tooltip": "Volver", "export_title": "Exportar Listas y Jugadores", "export_subtitle": "Guarda listas y jugadores en un archivo CSV.", "import_title": "Importar Listas y Jugadores", "import_subtitle": "Añade listas y jugadores desde un archivo CSV.", "save_file_dialog_title": "Guardar Archivo de Listas y Jugadores", "open_file_dialog_title": "Abrir Archivo de Listas y Jugadores", "import_dialog_title": "Modo de Importación", "import_dialog_content": "¿Qué hacer con los jugadores del archivo que ya existen en la aplicación?", "import_mode_ignore": "Ignorar", "import_mode_overwrite": "Sobrescribir", "continue_import_button": "Continuar Importación", "export_success": "¡Listas y jugadores exportados con éxito!", "export_error": "Error al exportar archivo: {error}", "import_summary": "Importación: {added_players} jugadores y {added_lists} listas creados. {updated_players} jugadores actualizados, {skipped_players} ignorados.", "import_error": "Error al importar archivo: {error}", "language_selection_label": "Idioma de la Aplicación:", "language_pt_br": "Portugués (Brasil)", "language_en_us": "Inglés (EE.UU.)", "language_es": "Español",
        
        # Legal Screens Links (Settings View)
        "privacy_policy_link_title": "Política de Privacidad",
        "terms_of_use_link_title": "Términos de Uso",
        
        # Legal Screens Titles & Content
        "privacy_policy_title": "Política de Privacidad",
        "terms_of_use_title": "Términos de Uso",
        
        # Selection View
        "selection_title": "Seleccionar Jugadores", "selected_players_count": "Jugadores seleccionados: {count}", "clear_button": "Limpiar", "teams_count": "{count} Equipos", "selection_error": "Verifique nº de equipos y jugadores.",

        # Results View
        "results_title": "Equipos Generados", "reorganize_button": "Reorganizar", "share_all_button": "Compartir Todos", "reorganizing_dialog_title": "Reorganizando...", "organizing_dialog_title": "Organizando...", "generate_teams_first_error": "¡Genera los equipos primero!", "all_teams_copied_success": "¡Todos los equipos copiados!", "team_copied_success": "¡Equipo {team_name} copiado!", "total_skill_label": "Habilidad Total:", "copy_button_tooltip": "Copiar {team_name}", "team_name_prefix": "Equipo {color_name}",
        
        # Manage Players View
        "manage_list_title": "Gestionando la Lista:", "rename_list_tooltip": "Renombrar Lista", "save_changes_button": "Guardar Cambios", "list_updated_success": "¡Lista actualizada con éxito!", "save_error": "Error al guardar: {error}",
    }
}

def get_string(state, key, default=None, **kwargs):
    """
    Obtém uma string traduzida do dicionário STRINGS usando o idioma
    atualmente definido no 'state'.
    Faz fallback para en_us se a chave não existir no idioma atual.
    Permite formatação com **kwargs.
    """
    language_dict = STRINGS.get(state.current_language, STRINGS["en_us"])
    
    # Tenta o idioma atual
    base_string = language_dict.get(key)
    
    # Se falhar, tenta o inglês
    if base_string is None:
        base_string = STRINGS["en_us"].get(key)
        
    # Se falhar, usa o 'default' ou a chave
    if base_string is None:
        base_string = default or f"_{key}_"

    try:
        # Usa defaultdict para evitar KeyErrors na formatação
        # caso uma kwarg não seja fornecida
        return base_string.format_map(defaultdict(str, **kwargs))
    except KeyError as e:
        print(f"Alerta: Chave de formatação ausente em '{key}' para idioma '{state.current_language}'. Esperava: {e}")
        return base_string # Retorna a string base sem formatação

def get_team_color_name(state, index):
    """
    Obtém o nome traduzido de uma cor de time com base no índice.
    """
    color_names = TEAM_COLORS.get(state.current_language, TEAM_COLORS["en_us"])
    return color_names[index % len(color_names)]