# views/privacy_policy_view.py
import flet as ft
from localization import get_string
import os 

def build_privacy_policy_view(state):
    """Constrói a view da Política de Privacidade."""

    def load_policy_content(lang_code):
        """Carrega o conteúdo do ficheiro markdown com base no idioma."""
        filename_map = {
            "pt_br": "privacy_policy_pt.md",
            "es": "privacy_policy_es.md",
            "en_us": "privacy_policy_en.md" 
        }
        filename = filename_map.get(lang_code, filename_map["en_us"])
        filepath = os.path.join("assets", filename)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"AVISO: Ficheiro de política de privacidade não encontrado: {filepath}")
            return f"Erro: Ficheiro '{filename}' não encontrado."
        except Exception as e:
            print(f"Erro ao ler ficheiro de política: {e}")
            return f"Erro ao carregar conteúdo: {e}"

    policy_text = load_policy_content(state.current_language)

    content = ft.Column(
        [
            ft.Markdown(
                policy_text,
                selectable=True,
                auto_follow_links=True 
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE, 
        expand=True,
        spacing=10
    )

    view = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.IconButton(
                        icon="arrow_back", # <--- CORREÇÃO DE ÍCONE
                        on_click=lambda e: state.navigate_to("settings"), 
                        tooltip=get_string(state, "back_button_tooltip")
                    ),
                    ft.Text(
                        get_string(state, "privacy_policy_title"),
                        size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(width=48)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Divider(),
            ft.Container(
                content=content, 
                expand=True,
                padding=ft.padding.symmetric(horizontal=15)
            )
        ],
        expand=True 
    )
    return view