# views/privacy_policy_view.py
import flet as ft
from localization import get_string

def build_privacy_policy_view(state):
    """Constrói a view da Política de Privacidade."""

    # Conteúdo de exemplo (pode usar ft.Markdown se preferir formatar)
    content = ft.Column(
        [
            ft.Text(get_string(state, "legal_content_placeholder"), selectable=True),
            # Adicione mais ft.Text ou outros controlos aqui conforme necessário
            # Ex: ft.Text("Seção 1: Informações Coletadas"), ft.Text("...")
        ],
        scroll=ft.ScrollMode.ADAPTIVE, # Usa ADAPTIVE para melhor rolagem
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
                        get_string(state, "privacy_policy_title"),
                        size=20, weight="bold", expand=True, text_align=ft.TextAlign.CENTER
                    ),
                    # Espaço reservado para manter o título centralizado
                    ft.Container(width=48)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Divider(),
            # Container para o conteúdo rolável
            ft.Container(
                content=content,
                expand=True,
                padding=ft.padding.symmetric(horizontal=15)
            )
        ],
        expand=True # Garante que a coluna principal ocupe todo o espaço
    )
    return view