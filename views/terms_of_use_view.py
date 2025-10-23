# views/terms_of_use_view.py
import flet as ft
from localization import get_string

def build_terms_of_use_view(state):
    """Constrói a view dos Termos de Uso."""

    # Conteúdo de exemplo
    content = ft.Column(
        [
            ft.Text(get_string(state, "legal_content_placeholder"), selectable=True),
            # Ex: ft.Text("Seção 1: Aceitação dos Termos"), ft.Text("...")
        ],
        scroll=ft.ScrollMode.ADAPTIVE, # Usa ADAPTIVE
        expand=True,
        spacing=10
    )

    view = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.IconButton(
                        icon="arrow_back",
                        on_click=lambda e: state.navigate_to("settings"), # Volta para Configurações
                        tooltip=get_string(state, "back_button_tooltip")
                    ),
                    ft.Text(
                        get_string(state, "terms_of_use_title"),
                        size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(width=48) # Espaço reservado
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
        expand=True # Garante que a coluna principal ocupe todo o espaço
    )
    return view