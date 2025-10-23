# app_state.py
import flet as ft
import os
import json
from localization import get_string
# Importa colors da maneira correta para Flet 0.25.x
# (Se ft.colors não funcionar, a biblioteca pode precisar de uma verificação mais aprofundada)

class AppState:
    """Classe para gerenciar o estado compartilhado do aplicativo."""
    def __init__(self, page):
        self.page = page

        # Caminho do arquivo de configuração
        self.config_file_path = os.path.join(os.path.expanduser("~"), ".organizador_de_times", "config.json")

        # --- CARREGA TODAS AS CONFIGURAÇÕES ---
        self.config = self._load_config()
        self.current_language = self.config.get("language", "pt_br")
        self.preferred_theme_mode = self.config.get("theme_mode", "dark") # Padrão dark se não salvo

        # --- USA OS VALORES CARREGADOS ---
        self.active_list_id = self.config.get("last_active_list_id", 0)
        self.preferred_team_count = self.config.get("last_team_count", 2)
        self.is_pro_user = self.config.get("is_pro", False)

        # --- O resto do estado ---
        self.photo_cache = {}
        self.resultado_times = []
        self.selecionados = []

        # --- Componentes da UI ---
        self.team_count_slider = ft.Slider(
            min=2, max=10, divisions=8,
            value=self.preferred_team_count,
            label="{value}", width=250
        )
        self.team_count_text = ft.Text("", size=16, weight="bold")
        # Atualiza o texto inicial após ter certeza que o idioma está carregado
        self.team_count_text.value = get_string(self, "teams_count", count=self.preferred_team_count)

        self.lists_dropdown = ft.Dropdown(expand=True)
        self.lista_jogadores = ft.ListView(expand=True, spacing=0, padding=0)
        self.loading_indicator = ft.ProgressRing(width=20, height=20, visible=False)
        self.filter_name_input = ft.TextField(border_radius=20, dense=True, expand=True)
        self.checkbox_list = ft.ListView(expand=True, spacing=0, padding=0)
        self.selected_count_text = ft.Text("")

        self.teams_layout_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

        self.theme_toggle_button = None
        self.input_container = None
        self.edit_container = None
        self.main_view_content = None
        self.list_management_menu = None
        self.organize_button = None

        self.navigate_to = None
        self.show_form = None
        self.hide_form = None
        self.show_edit_form = None
        self.montar_lista_jogadores = None
        self.reorganize_teams = None
        self.populate_lists_dropdown = None
        self.populate_new_player_lists_form = None
        self.open_rename_list_dialog = None

        self.rename_menu_item = None
        self.manage_menu_item = None
        self.delete_menu_item = None

    def _load_config(self):
        default_config = {
            "language": "pt_br",
            "theme_mode": "dark",
            "last_active_list_id": 0,
            "last_team_count": 2,
            "is_pro": False
        }
        try:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    config = default_config.copy(); config.update(loaded_config)
                    if config["language"] not in ["pt_br", "en_us", "es"]: config["language"] = default_config["language"]
                    if config["theme_mode"] not in ["dark", "light"]: config["theme_mode"] = default_config["theme_mode"]
                    if not isinstance(config.get("last_active_list_id"), int): config["last_active_list_id"] = default_config["last_active_list_id"]
                    if not isinstance(config.get("last_team_count"), int) or not (2 <= config["last_team_count"] <= 10): config["last_team_count"] = default_config["last_team_count"]
                    if not isinstance(config.get("is_pro"), bool): config["is_pro"] = default_config["is_pro"]
                    return config
            return default_config
        except Exception as e:
            print(f"Erro ao carregar config.json: {e}. Usando configuração padrão.")
            return default_config

    def save_config(self, key, value):
        try:
            current_config = self._load_config()
            current_config[key] = value
            os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(current_config, f, indent=4)
            # Atualiza estado interno
            if key == "is_pro": self.is_pro_user = value
            elif key == "language": self.current_language = value
            elif key == "theme_mode": self.preferred_theme_mode = value
            elif key == "last_active_list_id": self.active_list_id = value
            elif key == "last_team_count": self.preferred_team_count = value
        except Exception as e:
            print(f"Erro ao salvar configuração ({key}): {e}")

    def purchase_pro_placeholder(self):
        """Simula a compra da versão Pro."""
        if not self.is_pro:
            print("Simulando compra Pro...")
            self.save_pro_status(True)
            if self.page:
                 self.page.show_snack_bar(ft.SnackBar(
                     ft.Text(get_string(self, "pro_activated_success")),
                     bgcolor=ft.colors.GREEN_700, # Usa ft.colors.
                     open=True
                 ))
                 if self.page.route:
                     current_view = self.page.route.strip('/')
                     self.navigate_to(current_view if current_view else "main")
        else:
             print("Usuário já é Pro.")
             if self.page:
                 self.page.show_snack_bar(ft.SnackBar(
                     ft.Text(get_string(self, "already_pro")),
                     open=True
                 ))

    def deactivate_pro_placeholder(self):
        """Simula a desativação da versão Pro (apenas para teste)."""
        if self.is_pro:
            print("Desativando Pro (Teste)...")
            self.save_pro_status(False)
            if self.page:
                self.page.show_snack_bar(ft.SnackBar(
                    ft.Text(get_string(self, "pro_deactivated_success")),
                    bgcolor=ft.colors.AMBER_700, # Usa ft.colors.
                    open=True
                ))
                if self.page.route:
                    current_view = self.page.route.strip('/')
                    self.navigate_to(current_view if current_view else "main")
        else:
            print("Usuário já está na versão gratuita.")

    def save_language_preference(self, lang_code): self.save_config("language", lang_code)
    def save_theme_preference(self, theme_mode): self.save_config("theme_mode", theme_mode)
    def save_last_list_preference(self, list_id): self.save_config("last_active_list_id", list_id)
    def save_last_team_count_preference(self, count): self.save_config("last_team_count", count)
    def save_pro_status(self, is_pro: bool): self.save_config("is_pro", is_pro)

    @property
    def is_pro(self) -> bool: return self.is_pro_user

    def update(self):
        if self.page: self.page.update()