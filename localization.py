# localization.py

TEAM_COLORS = {
    "pt_br": ["Vermelho", "Azul", "Verde", "Amarelo", "Roxo", "Laranja", "Ciano", "Rosa", "Verde Limão", "Índigo"],
    "en_us": ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Cyan", "Pink", "Lime Green", "Indigo"],
    "es": ["Rojo", "Azul", "Verde", "Amarillo", "Morado", "Naranja", "Cian", "Rosa", "Verde Lima", "Índigo"],
}

STRINGS = {
    "pt_br": {
        # Main View & Menus
        "app_title": "Organizador de Times", "toggle_theme_tooltip": "Alternar Tema", "settings_tooltip": "Configurações", "select_list_label": "Selecione a Lista:", "organize_button_text": "Organizar Times", "organize_button_tooltip_disabled": "Selecione uma lista específica para poder organizar os times", "register_player_button_text": "Cadastrar Jogador", "filter_by_name_label": "Filtrar por Nome...", "all_players_list_name": "Jogadores Cadastrados", "create_new_list_menu": "Criar nova lista", "rename_list_menu": "Renomear lista atual", "manage_players_menu": "Gerenciar Jogadores", "delete_list_menu": "Excluir lista atual",
        # Components (Formulários & Diálogos)
        "player_name_label": "Nome", "name_cannot_be_empty_error": "O nome não pode estar vazio", "select_at_least_one_list_error": "Selecione pelo menos uma lista!", "player_saved_success": "Cadastrado com sucesso", "player_updated_success": "Jogador atualizado!", "generic_error": "Erro ao cadastrar: {error}", "new_player_title": "Novo Jogador", "edit_player_title": "Editar Jogador", "choose_photo_button": "Escolher Foto", "change_photo_button": "Mudar Foto", "skill_label": "Skill:", "add_to_lists_label": "Adicionar às Listas:", "save_player_button": "Salvar Jogador", "update_button": "Atualizar", "delete_confirmation_title": "Confirmação de Exclusão", "delete_player_confirmation_content": "Tem certeza que deseja excluir este jogador?", "delete_list_confirmation_content": "Tem certeza que deseja apagar a lista '{list_name}'?", "yes_button": "Sim", "no_button": "Não", "cancel_button": "Cancelar", "save_button": "Salvar", "player_deleted_success": "Jogador excluído!", "edit_tooltip": "Editar", "delete_tooltip": "Excluir", "empty_state_title": "Nenhum jogador por aqui...", "empty_state_subtitle1": "Clique em 'Cadastrar Jogador' para adicionar o primeiro!", "empty_state_subtitle2": "Ou use o menu (⋮) e 'Gerenciar Jogadores' para adicionar jogadores já existentes a esta lista.",
        # Dialogs
        "create_list_dialog_title": "Criar Nova Lista", "new_list_name_label": "Nome da Nova Lista", "list_already_exists_error": "Esta lista já existe.", "rename_list_dialog_title": "Renomear Lista", "new_list_name_label_edit": "Novo nome da lista", "list_renamed_success": "Lista renomeada com sucesso!", "cannot_delete_last_list_error": "Não é possível apagar a última lista.",
        # Settings View
        "settings_title": "Configurações", "back_button_tooltip": "Voltar", "export_title": "Exportar Listas e Jogadores", "export_subtitle": "Salva listas e jogadores em um arquivo CSV.", "import_title": "Importar Listas e Jogadores", "import_subtitle": "Adiciona listas e jogadores de um arquivo CSV.", "save_file_dialog_title": "Salvar Arquivo de Listas e Jogadores", "open_file_dialog_title": "Abrir Arquivo de Listas e Jogadores", "import_dialog_title": "Modo de Importação", "import_dialog_content": "O que fazer com jogadores do arquivo que já existem no app?", "import_mode_ignore": "Ignorar", "import_mode_overwrite": "Sobrescrever", "continue_import_button": "Continuar Importação", "export_success": "Listas e jogadores exportados com sucesso!", "export_error": "Erro ao exportar arquivo: {error}", "import_summary": "Importação: {added_players} jogadores e {added_lists} listas criados. {updated_players} jogadores atualizados, {skipped_players} ignorados.", "import_error": "Erro ao importar arquivo: {error}", "language_selection_label": "Idioma do Aplicativo:", "language_pt_br": "Português (Brasil)", "language_en_us": "Inglês (EUA)", "language_es": "Espanhol",
        # Pro Version & Limitations
        "# Pro Version & Limitations": "", "become_pro_title": "Tornar-se Pro (Desbloquear Tudo)", "become_pro_subtitle": "Remove limitações. (Status: {status})", # Removido "anúncios"
        "restore_purchases_title": "Restaurar Compras", "restore_purchases_subtitle": "Já comprou? Reative a versão Pro aqui.", "pro_activated_success": "Versão Pro ativada!", "already_pro": "Você já possui a Versão Pro!", "deactivate_pro_title": "Desativar Pro (Teste)", "deactivate_pro_subtitle": "Volta para a versão gratuita para testes.", "pro_deactivated_success": "Versão Pro desativada.", "status_pro": "Ativo", "status_free": "Gratuito",
        "limit_reached_title": "Limite Atingido",
        "list_limit_reached_message": "A versão gratuita permite criar até {limit} listas personalizadas. Atualize para Pro para listas ilimitadas!",
        "player_limit_reached_message": "A versão gratuita permite cadastrar até {limit} jogadores. Atualize para Pro para jogadores ilimitados!",
        "team_limit_reached_message": "A versão gratuita permite organizar até {limit} times. Atualize para Pro para mais times!",
        "daily_organization_limit_reached_title": "Limite de Organizações Atingido",
        "daily_organization_limit_reached_message": "Organizações/Reorganizações adicionais requerem a Versão Pro. Atualize para uso ilimitado!", # Ajustado
        # "watch_ad_button": "Assistir Anúncio", # REMOVIDO
        "feature_for_pro_title": "Funcionalidade Pro",
        "sharing_pro_feature_message": "Compartilhar times é uma funcionalidade exclusiva da versão Pro.",
        "import_export_pro_feature_message": "Importar e Exportar dados é uma funcionalidade exclusiva da versão Pro.",
        "upgrade_button": "Atualizar para Pro",
        # Selection View
        "selection_title": "Selecionar Jogadores", "selected_players_count": "Jogadores selecionados: {count}", "clear_button": "Limpar", "teams_count": "{count} Times",
        # Results View
        "results_title": "Times Gerados", "reorganize_button": "Reorganizar", "share_all_button": "Compartilhar Todos", "reorganizing_dialog_title": "Reorganizando...", "organizing_dialog_title": "Organizando...", "generate_teams_first_error": "Gere os times primeiro!", "all_teams_copied_success": "Times copiados!", "team_copied_success": "{team_name} copiado!", "total_skill_label": "Total Skill:", "copy_button_tooltip": "Copiar {team_name}", "team_name_prefix": "Time {color_name}",
        # Manage Players View
        "manage_list_title": "Gerenciando a Lista:", "rename_list_tooltip": "Renomear Lista", "save_changes_button": "Salvar Alterações", "list_updated_success": "Lista atualizada com sucesso!", "save_error": "Erro ao salvar: {error}",
    },
    "en_us": {
        # Main View & Menus
        "app_title": "Team Organizer", "toggle_theme_tooltip": "Toggle Theme", "settings_tooltip": "Settings", "select_list_label": "Select a List:", "organize_button_text": "Organize Teams", "organize_button_tooltip_disabled": "Select a specific list to organize teams", "register_player_button_text": "Register Player", "filter_by_name_label": "Filter by Name...", "all_players_list_name": "All Registered Players", "create_new_list_menu": "Create new list", "rename_list_menu": "Rename current list", "manage_players_menu": "Manage Players", "delete_list_menu": "Delete current list",
        # Components (Formulários & Diálogos)
        "player_name_label": "Name", "name_cannot_be_empty_error": "Name cannot be empty", "select_at_least_one_list_error": "Select at least one list!", "player_saved_success": "Registered successfully", "player_updated_success": "Player updated!", "generic_error": "Error while saving: {error}", "new_player_title": "New Player", "edit_player_title": "Edit Player", "choose_photo_button": "Choose Photo", "change_photo_button": "Change Photo", "skill_label": "Skill:", "add_to_lists_label": "Add to Lists:", "save_player_button": "Save Player", "update_button": "Update", "delete_confirmation_title": "Delete Confirmation", "delete_player_confirmation_content": "Are you sure you want to delete this player?", "delete_list_confirmation_content": "Are you sure you want to delete the list '{list_name}'?", "yes_button": "Yes", "no_button": "No", "cancel_button": "Cancel", "save_button": "Save", "player_deleted_success": "Player deleted!", "edit_tooltip": "Edit", "delete_tooltip": "Delete", "empty_state_title": "No players around here...", "empty_state_subtitle1": "Click 'Register Player' to add the first one!", "empty_state_subtitle2": "Or use the (⋮) menu and 'Manage Players' to add existing players to this list.",
        # Dialogs
        "create_list_dialog_title": "Create New List", "new_list_name_label": "New List Name", "list_already_exists_error": "This list already exists.", "rename_list_dialog_title": "Rename List", "new_list_name_label_edit": "New list name", "list_renamed_success": "List renamed successfully!", "cannot_delete_last_list_error": "Cannot delete the last list.",
        # Settings View
        "settings_title": "Settings", "back_button_tooltip": "Back", "export_title": "Export Lists and Players", "export_subtitle": "Saves lists and players to a CSV file.", "import_title": "Import Lists and Players", "import_subtitle": "Adds lists and players from a CSV file.", "save_file_dialog_title": "Save Lists and Players File", "open_file_dialog_title": "Open Lists and Players File", "import_dialog_title": "Import Mode", "import_dialog_content": "What to do with players from the file that already exist in the app?", "import_mode_ignore": "Ignore", "import_mode_overwrite": "Overwrite", "continue_import_button": "Continue Import", "export_success": "Lists and players exported successfully!", "export_error": "Error exporting file: {error}", "import_summary": "Import: {added_players} players and {added_lists} lists created. {updated_players} players updated, {skipped_players} skipped.", "import_error": "Error importing file: {error}", "language_selection_label": "App Language:", "language_pt_br": "Portuguese (Brazil)", "language_en_us": "English (US)", "language_es": "Spanish",
        # Pro Version & Limitations
        "# Pro Version & Limitations": "", "become_pro_title": "Become Pro (Unlock Everything)", "become_pro_subtitle": "Removes limitations. (Status: {status})", # Removed "ads"
        "restore_purchases_title": "Restore Purchases", "restore_purchases_subtitle": "Already purchased? Reactivate Pro here.", "pro_activated_success": "Pro Version activated!", "already_pro": "You already have the Pro Version!", "deactivate_pro_title": "Deactivate Pro (Testing)", "deactivate_pro_subtitle": "Reverts to the free version for testing.", "pro_deactivated_success": "Pro Version deactivated.", "status_pro": "Active", "status_free": "Free",
        "limit_reached_title": "Limit Reached",
        "list_limit_reached_message": "The free version allows up to {limit} custom lists. Upgrade to Pro for unlimited lists!",
        "player_limit_reached_message": "The free version allows up to {limit} players. Upgrade to Pro for unlimited players!",
        "team_limit_reached_message": "The free version allows organizing up to {limit} teams. Upgrade to Pro for more teams!",
        "daily_organization_limit_reached_title": "Organization Limit Reached",
        "daily_organization_limit_reached_message": "Additional organizations/reorganizations require the Pro Version. Upgrade for unlimited use!", # Adjusted
        # "watch_ad_button": "Watch Ad", # REMOVED
        "feature_for_pro_title": "Pro Feature",
        "sharing_pro_feature_message": "Sharing teams is a Pro feature.",
        "import_export_pro_feature_message": "Importing and Exporting data is a Pro feature.",
        "upgrade_button": "Upgrade to Pro",
        # Selection View
        "selection_title": "Select Players", "selected_players_count": "Players selected: {count}", "clear_button": "Clear", "teams_count": "{count} Teams",
        # Results View
        "results_title": "Generated Teams", "reorganize_button": "Reorganize", "share_all_button": "Share All", "reorganizing_dialog_title": "Reorganizing...", "organizing_dialog_title": "Organizing...", "generate_teams_first_error": "Generate the teams first!", "all_teams_copied_success": "Teams copied!", "team_copied_success": "{team_name} copied!", "total_skill_label": "Total Skill:", "copy_button_tooltip": "Copy {team_name}", "team_name_prefix": "Team {color_name}",
        # Manage Players View
        "manage_list_title": "Managing List:", "rename_list_tooltip": "Rename List", "save_changes_button": "Save Changes", "list_updated_success": "List updated successfully!", "save_error": "Error while saving: {error}",
    },
    "es": {
        # Main View & Menus
        "app_title": "Organizador de Equipos", "toggle_theme_tooltip": "Cambiar Tema", "settings_tooltip": "Configuración", "select_list_label": "Selecciona la Lista:", "organize_button_text": "Organizar Equipos", "organize_button_tooltip_disabled": "Selecciona una lista específica para organizar equipos", "register_player_button_text": "Registrar Jugador", "filter_by_name_label": "Filtrar por Nombre...", "all_players_list_name": "Todos los Jugadores", "create_new_list_menu": "Crear nueva lista", "rename_list_menu": "Renombrar lista actual", "manage_players_menu": "Gestionar Jugadores", "delete_list_menu": "Eliminar lista actual",
        # Components (Formulários & Diálogos)
        "player_name_label": "Nombre", "name_cannot_be_empty_error": "El nombre no puede estar vacío", "select_at_least_one_list_error": "¡Selecciona al menos una lista!", "player_saved_success": "Registrado con éxito", "player_updated_success": "¡Jugador actualizado!", "generic_error": "Error al registrar: {error}", "new_player_title": "Nuevo Jugador", "edit_player_title": "Editar Jugador", "choose_photo_button": "Elegir Foto", "change_photo_button": "Cambiar Foto", "skill_label": "Habilidad:", "add_to_lists_label": "Añadir a Listas:", "save_player_button": "Guardar Jugador", "update_button": "Actualizar", "delete_confirmation_title": "Confirmar Eliminación", "delete_player_confirmation_content": "¿Estás seguro de que quieres eliminar a este jugador?", "delete_list_confirmation_content": "¿Estás seguro de que quieres borrar la lista '{list_name}'?", "yes_button": "Sí", "no_button": "No", "cancel_button": "Cancelar", "save_button": "Guardar", "player_deleted_success": "¡Jugador eliminado!", "edit_tooltip": "Editar", "delete_tooltip": "Eliminar", "empty_state_title": "No hay jugadores por aquí...", "empty_state_subtitle1": "¡Haz clic en 'Registrar Jugador' para añadir el primero!", "empty_state_subtitle2": "O usa el menú (⋮) y 'Gestionar Jugadores' para añadir jugadores existentes a esta lista.",
        # Dialogs
        "create_list_dialog_title": "Crear Nueva Lista", "new_list_name_label": "Nombre de la Nueva Lista", "list_already_exists_error": "Esta lista ya existe.", "rename_list_dialog_title": "Renombrar Lista", "new_list_name_label_edit": "Nuevo nombre de la lista", "list_renamed_success": "¡Lista renombrada con éxito!", "cannot_delete_last_list_error": "No se puede borrar la última lista.",
        # Settings View
        "settings_title": "Configuración", "back_button_tooltip": "Volver", "export_title": "Exportar Listas y Jugadores", "export_subtitle": "Guarda listas y jugadores en un archivo CSV.", "import_title": "Importar Listas y Jugadores", "import_subtitle": "Añade listas y jugadores desde un archivo CSV.", "save_file_dialog_title": "Guardar Archivo de Listas y Jugadores", "open_file_dialog_title": "Abrir Archivo de Listas y Jugadores", "import_dialog_title": "Modo de Importación", "import_dialog_content": "¿Qué hacer con los jugadores del archivo que ya existen en la aplicación?", "import_mode_ignore": "Ignorar", "import_mode_overwrite": "Sobrescribir", "continue_import_button": "Continuar Importación", "export_success": "¡Listas y jugadores exportados con éxito!", "export_error": "Error al exportar archivo: {error}", "import_summary": "Importación: {added_players} jugadores y {added_lists} listas creados. {updated_players} jugadores actualizados, {skipped_players} ignorados.", "import_error": "Error al importar archivo: {error}", "language_selection_label": "Idioma de la Aplicación:", "language_pt_br": "Portugués (Brasil)", "language_en_us": "Inglés (EE.UU.)", "language_es": "Español",
        # Pro Version & Limitations
        "# Pro Version & Limitations": "", "become_pro_title": "Hazte Pro (Desbloquear Todo)", "become_pro_subtitle": "Elimina limitaciones. (Estado: {status})", # Eliminado "anuncios"
        "restore_purchases_title": "Restaurar Compras", "restore_purchases_subtitle": "¿Ya compraste? Reactiva la versión Pro aquí.", "pro_activated_success": "¡Versión Pro activada!", "already_pro": "¡Ya tienes la Versión Pro!", "deactivate_pro_title": "Desactivar Pro (Prueba)", "deactivate_pro_subtitle": "Vuelve a la versión gratuita para pruebas.", "pro_deactivated_success": "Versión Pro desactivada.", "status_pro": "Activo", "status_free": "Gratis",
        "limit_reached_title": "Límite Alcanzado",
        "list_limit_reached_message": "¡La versión gratuita permite hasta {limit} listas personalizadas. Actualiza a Pro para listas ilimitadas!",
        "player_limit_reached_message": "¡La versión gratuita permite hasta {limit} jugadores. Actualiza a Pro para jugadores ilimitados!",
        "team_limit_reached_message": "¡La versión gratuita permite organizar hasta {limit} equipos. Actualiza a Pro para más equipos!",
        "daily_organization_limit_reached_title": "Límite de Organizaciones Alcanzado",
        "daily_organization_limit_reached_message": "Organizaciones/Reorganizaciones adicionales requieren la Versión Pro. ¡Actualiza para uso ilimitado!", # Ajustado
        # "watch_ad_button": "Ver Anuncio", # ELIMINADO
        "feature_for_pro_title": "Función Pro",
        "sharing_pro_feature_message": "Compartir equipos es una función exclusiva de la versión Pro.",
        "import_export_pro_feature_message": "Importar y Exportar datos es una función exclusiva de la versión Pro.",
        "upgrade_button": "Actualizar a Pro",
        # Selection View
        "selection_title": "Seleccionar Jugadores", "selected_players_count": "Jugadores seleccionados: {count}", "clear_button": "Limpiar", "teams_count": "{count} Equipos",
        # Results View
        "results_title": "Equipos Generados", "reorganize_button": "Reorganizar", "share_all_button": "Compartir Todos", "reorganizing_dialog_title": "Reorganizando...", "organizing_dialog_title": "Organizando...", "generate_teams_first_error": "¡Genera los equipos primero!", "all_teams_copied_success": "¡Equipos copiados!", "team_copied_success": "¡Equipo {team_name} copiado!", "total_skill_label": "Habilidad Total:", "copy_button_tooltip": "Copiar {team_name}", "team_name_prefix": "Equipo {color_name}",
        # Manage Players View
        "manage_list_title": "Gestionando la Lista:", "rename_list_tooltip": "Renombrar Lista", "save_changes_button": "Guardar Cambios", "list_updated_success": "¡Lista actualizada con éxito!", "save_error": "Error al guardar: {error}",
    }
}

def get_string(state, key, **kwargs):
    language_dict = STRINGS.get(state.current_language, STRINGS["en_us"])
    base_string = language_dict.get(key, STRINGS["en_us"].get(key, f"_{key}_"))
    try: return base_string.format(**kwargs)
    except KeyError: print(f"Alerta: Chave de formatação ausente em '{key}' para idioma '{state.current_language}'"); return base_string
def get_team_color_name(state, index):
    color_names = TEAM_COLORS.get(state.current_language, TEAM_COLORS["en_us"])
    return color_names[index % len(color_names)]