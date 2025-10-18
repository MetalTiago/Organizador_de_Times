# app_state.py
import flet as ft

class AppState:
    """Classe para gerenciar o estado compartilhado do aplicativo."""
    def __init__(self, page):
        self.page = page
        

        self.current_language = "en_us"
        # --- AQUI ESTÁ A MUDANÇA ---
        # A lista ativa ao iniciar agora é a 0 ("Jogadores Cadastrados")

        self.active_list_id = 0
        
        # --- O resto do estado ---
        self.photo_cache = {}
        self.resultado_times = []
        self.selecionados = []
        
        # --- Componentes da UI ---
        self.lists_dropdown = ft.Dropdown(expand=True)
        self.lista_jogadores = ft.ListView(expand=True, spacing=0, padding=0)
        self.loading_indicator = ft.ProgressRing(width=20, height=20, visible=False)
        self.filter_name_input = ft.TextField(label="Filtrar por Nome...", border_radius=20, dense=True, expand=True)
        self.checkbox_list = ft.ListView(expand=True, spacing=0, padding=0)
        self.selected_count_text = ft.Text("Jogadores selecionados: 0")
        self.team_count_text = ft.Text("2 Times", size=16, weight="bold")
        self.team_count_slider = ft.Slider(min=2, max=10, divisions=8, value=2, label="{value}", width=250)
        self.teams_layout_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
        
        self.theme_toggle_button = None
        self.input_container = None
        self.edit_container = None
        self.main_view_content = None
        self.list_management_menu = None 
        
        self.navigate_to = None
        self.show_form = None
        self.hide_form = None
        self.show_edit_form = None
        self.montar_lista_jogadores = None
        self.reorganize_teams = None
        self.populate_lists_dropdown = None
        self.populate_new_player_lists_form = None
        self.open_rename_list_dialog = None

        # --- Referências de Itens de Menu ---
        self.rename_menu_item = None
        self.manage_menu_item = None
        self.delete_menu_item = None

        self.organize_button = None

    # --- MÉTODO UPDATE ADICIONADO ---
    # Este método permite que outras partes do código chamem a atualização da página
    # de uma forma mais limpa, através do objeto de estado.
    def update(self):
        self.page.update()