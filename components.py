from flet import *
import flet as ft
from db_handler import get_all_users, delete_user, update_user

# Variável global para a página, será setada na main.py
page_ref = None

tb = DataTable(
    columns=[
        DataColumn(Text("Nome")),
        DataColumn(Text("Skill")),
        DataColumn(Text("Ação")),
    ],
    rows=[],
)

# --- Definição dos Controles do Diálogo de Edição ---
txt_skill_data = Text("0", size=20)
id_edit = Text() # Para armazenar o ID do usuário sendo editado (não visível, mas usado na lógica)
name_edit = TextField(label="Nome")
# Corrigido: Removido expand=True do Slider
skill_edit = Slider(min=0, max=10, divisions=10, label="{value}")

# Cartão que representa a interface visual do diálogo de edição
edit_card = ft.Card(
    elevation=30,
    width=380, # Largura do diálogo
    # O conteúdo do Card (a Coluna com os campos) será definido abaixo
)

# Container 'dlg' que vai para o overlay. Ele centraliza o 'edit_card'.
dlg = ft.Container(
    content=edit_card,
    visible=False,
    alignment=ft.alignment.center, # Centraliza o edit_card na tela
    # Opcional: Adicionar um leve escurecimento ao fundo do overlay quando o diálogo está visível
    # bgcolor=ft.colors.with_opacity(0.3, ft.colors.BLACK), # Exemplo
)

# Definindo o conteúdo do edit_card (a coluna de formulário)
edit_card.content = ft.Container( # Envolve a coluna com um Container para adicionar padding interno ao Card
    padding=20, # Padding interno do Card
    content=ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Editar Jogador", size=20, weight="bold"),
                    ft.IconButton(icon="close", on_click=lambda e: hidedlg(e), icon_color=ft.colors.ON_SURFACE),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            name_edit,
            ft.Row([ft.Text("Skill", size=20), txt_skill_data]),
            skill_edit, # Agora sem expand=True
            ft.Container(
                content=ft.ElevatedButton("Atualizar", on_click=lambda e: updateandsave(e)),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=15) # Espaçamento antes do botão
            ),
        ],
        spacing=15, # Espaçamento entre os elementos da coluna
        tight=True, # Faz a coluna se ajustar à altura do seu conteúdo
    )
)

# --- Fim da Definição dos Controles do Diálogo de Edição ---

# Diálogo de confirmação de exclusão (como estava)
confirm_dlg = ft.AlertDialog(
    modal=True,
    title=ft.Text("Confirmação de Exclusão"),
    content=ft.Text("Tem certeza que deseja excluir este jogador?"),
    actions=[
        ft.TextButton("Sim", on_click=lambda e: confirm_delete(e, True), style=ft.ButtonStyle(color=ft.colors.PRIMARY)),
        ft.TextButton("Não", on_click=lambda e: confirm_delete(e, False), style=ft.ButtonStyle(color=ft.colors.ON_SURFACE)),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

# Filtros
filter_name_input = TextField(label="Filtrar por Nome", on_change=lambda e: atualizar_tabela(apply_filters=True))

# Indicador de carregamento
loading_indicator = ft.ProgressRing(width=20, height=20, visible=False)


def set_page_ref(page):
    global page_ref
    page_ref = page
    page_ref.overlay.append(confirm_dlg)
    page_ref.overlay.append(dlg) # Adiciona o container do diálogo de edição ao overlay
    # page_ref.update() # Opcional aqui, se a página for atualizada após toda a configuração inicial.
                      # Pode manter se já estava funcionando bem.


def cor_skill(n):
    n = int(n)
    if 4 < n < 7:  # Skills 5, 6
        return ft.colors.RED_ACCENT_400
    elif 6 < n < 9:  # Skills 7, 8
        return ft.colors.YELLOW_ACCENT_400
    elif n >= 9:  # Skills 9, 10
        return ft.colors.BLUE_ACCENT_400
    return ft.colors.ON_SURFACE # Cor dinâmica para skills 0-4


def atualizar_tabela(sort_column=None, sort_ascending=True, apply_filters=False):
    loading_indicator.visible = True
    tb.visible = False
    if page_ref:
        page_ref.update()

    tb.rows.clear()
    users = get_all_users()

    if apply_filters:
        name_filter = filter_name_input.value.lower()
        filtered_users = [user for user in users if name_filter in user[1].lower()]
        users = filtered_users

    if sort_column == "name":
        users.sort(key=lambda x: x[1], reverse=not sort_ascending)
    elif sort_column == "skill":
        users.sort(key=lambda x: x[2], reverse=not sort_ascending)
    else:
        users.sort(key=lambda x: x[0])

    for user in users:
        user_dict = {"id": user[0], "name": user[1], "skill": user[2]}
        tb.rows.append(
            DataRow(
                cells=[
                    DataCell(Text(user_dict["name"])),
                    DataCell(Text(str(user_dict["skill"]), color=cor_skill(user_dict["skill"]))),
                    DataCell(
                        Row(
                            [
                                IconButton(icon=ft.icons.CREATE, icon_color=ft.colors.BLUE_ACCENT_400, data=user_dict, on_click=showedit),
                                IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.RED_ACCENT_400, data=user_dict["id"], on_click=showdelete_confirm),
                            ]
                        )
                    ),
                ]
            )
        )
    loading_indicator.visible = False
    tb.visible = True
    if page_ref:
        page_ref.update()
    # tb.update() # tb.update() é chamado por page_ref.update() se tb estiver na página.

def sort_table(e, column_name):
    if tb.sort_column_index is None or tb.sort_column_index != (0 if column_name == "name" else 1):
        tb.sort_ascending = True
    else:
        tb.sort_ascending = not tb.sort_ascending
    
    tb.sort_column_index = (0 if column_name == "name" else 1)
    atualizar_tabela(sort_column=column_name, sort_ascending=tb.sort_ascending)

def showedit(e):
    user = e.control.data
    id_edit.value = str(user["id"])
    name_edit.value = user["name"]
    skill_edit.value = float(user["skill"])
    txt_skill_data.value = str(int(skill_edit.value))
    txt_skill_data.color = cor_skill(skill_edit.value)
    
    dlg.visible = True
    if page_ref:
        page_ref.update()

def showdelete_confirm(e):
    confirm_dlg.open = True
    confirm_dlg.data = e.control.data
    if page_ref:
        page_ref.update()

def confirm_delete(e, confirmed):
    confirm_dlg.open = False
    if confirmed:
        user_id = confirm_dlg.data
        delete_user(user_id)
        atualizar_tabela()
        if page_ref:
            page_ref.snack_bar = ft.SnackBar(ft.Text("Jogador excluído com sucesso!"), bgcolor=ft.colors.GREEN_700)
            page_ref.snack_bar.open = True
    if page_ref: # Atualiza para fechar o AlertDialog visualmente
        page_ref.update()

def updateandsave(e):
    update_user(int(id_edit.value), name_edit.value, int(skill_edit.value))
    dlg.visible = False # Esconde o diálogo
    atualizar_tabela() # Atualiza a tabela (que também chama page_ref.update())
    if page_ref:
        page_ref.snack_bar = ft.SnackBar(ft.Text("Jogador atualizado com sucesso!"), bgcolor=ft.colors.GREEN_700)
        page_ref.snack_bar.open = True
        page_ref.update() # Garante que o snackbar e o diálogo escondido sejam atualizados

def hidedlg(e):
    dlg.visible = False
    if page_ref:
        page_ref.update()

def lbl_skill_data(e): # Chamado quando o slider do diálogo de edição muda
    txt_skill_data.value = f"{int(e.control.value)}"
    txt_skill_data.color = cor_skill(e.control.value)
    if dlg.visible and page_ref: # Se o diálogo estiver visível, atualize a página para refletir a mudança no txt_skill_data
        page_ref.update()

skill_edit.on_change = lbl_skill_data # Conecta o evento on_change do slider à função

mytable = ft.Column([
    ft.Row([filter_name_input], alignment=ft.MainAxisAlignment.START),
    ft.Row([loading_indicator, tb], alignment=ft.alignment.center)
], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
