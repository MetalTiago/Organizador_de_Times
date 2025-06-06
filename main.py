import flet as ft
from flet import *
from db_handler import create_table, insert_user, get_user_count
from components import mytable, atualizar_tabela, set_page_ref
from organizer import organizar_times
from db_handler import get_all_users
import asyncio

def main(page: ft.Page):
    page.title = "Organizador de Times"
    page.scroll = "auto"
    page.window_height = 840
    page.window_width = 400
    page.padding = 10

    # 1. Definir Temas Claro e Escuro
    page.theme = ft.Theme(
        color_scheme_seed="blue", # Uma cor base para gerar o esquema de cores do tema claro
        font_family="Roboto",
    )
   # page.dark_theme CORRIGIDO para Flet 0.22.0
    dark_theme_obj = ft.Theme(
        color_scheme_seed="blue",
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE_ACCENT_400,
            on_primary=ft.colors.WHITE,
            surface=ft.colors.GREY_900,
            on_surface=ft.colors.WHITE,
            surface_variant=ft.colors.GREY_800,
            on_surface_variant=ft.colors.WHITE,
            background=ft.colors.BLACK54,
            on_background=ft.colors.WHITE,
            error=ft.colors.RED_ACCENT_700,
            on_error=ft.colors.WHITE,
        ),
        font_family="Roboto",
    )
    dark_theme_obj.brightness = ft.Brightness.DARK # Define 'brightness' como uma propriedade
    page.dark_theme = dark_theme_obj

    page.theme_mode = "dark"
    page.bgcolor = None


    set_page_ref(page)

    create_table()

    def toggle_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    theme_toggle_button = IconButton(
        icon=ft.icons.WB_SUNNY if page.theme_mode == "light" else ft.icons.NIGHTS_STAY,
        tooltip="Alternar Tema",
        on_click=toggle_theme,
        icon_color=ft.colors.ON_SURFACE # Corrigido: usar icon_color
    )

    def update_theme_icon(e):
        theme_toggle_button.icon = ft.icons.WB_SUNNY if page.theme_mode == "light" else ft.icons.NIGHTS_STAY
        theme_toggle_button.icon_color = ft.colors.ON_SURFACE # Corrigido: usar icon_color
        page.update()
    
    page.on_theme_mode_change = update_theme_icon

    def show_form(e):
        input_container.visible = True
        name_input.value = ''
        name_input.error_text = None
        skill_slider.value = 0
        skill_text.value = '0'
        register_button.visible = False
        page.update()

    def hide_form(e):
        input_container.visible = False
        register_button.visible = True
        page.update()

    def update_skill_label(e):
        skill_text.value = f"{e.control.value:n}"
        page.update()

    def save_user(e):
        if not name_input.value:
            name_input.error_text = "O nome não pode estar vazio"
            page.update()
            return

        try:
            insert_user(name_input.value, int(skill_slider.value))
            page.snack_bar = ft.SnackBar(ft.Text("Cadastrado com sucesso"), bgcolor=ft.colors.GREEN_700)
            page.snack_bar.open = True
            atualizar_tabela()
            name_input.value = ''
            name_input.error_text = None
            skill_slider.value = 0
            skill_text.value = '0'
            hide_form(e)
        except Exception as ex:
            print("Erro ao salvar:", ex)
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao cadastrar: {ex}"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()

    name_input = ft.TextField(label="Nome")
    skill_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}", expand=True, on_change=update_skill_label)
    skill_text = ft.Text("0", size=20)

    input_container = ft.Card(
        visible=False,
        elevation=30,
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Novo Jogador", size=20, weight="bold"),
                    ft.IconButton(icon="close", icon_size=30, on_click=hide_form, icon_color=ft.colors.ON_SURFACE) # Corrigido: usar icon_color
                ], alignment="spaceBetween"),
                name_input,
                ft.Row([ft.Text("Skill", size=20), skill_text], spacing=20),
                skill_slider,
                ft.Container(content=ft.FilledButton("Salvar", on_click=save_user), alignment=ft.alignment.center, padding=10)
            ]),
            alignment=ft.alignment.center
        )
    )

    register_button = ft.ElevatedButton("Cadastrar", on_click=show_form, icon=ft.icons.ADD)

    selecionados = []
    checkbox_list = ft.Column(scroll=ft.ScrollMode.AUTO)
    radio_times = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(label="2 Times", value="2"),
            ft.Radio(label="3 Times", value="3"),
            ft.Radio(label="4 Times", value="4"),
        ])
    )
    selected_count_text = ft.Text("Jogadores selecionados: 0")

    def montar_lista_jogadores():
        checkbox_list.controls.clear()
        for jogador in get_all_users():
            is_selected = any(s[0] == jogador[0] for s in selecionados)
            cb = ft.Checkbox(label=f"{jogador[1]} (Skill: {jogador[2]})", value=is_selected, data=jogador, on_change=selecionar_jogador,
                             fill_color=ft.colors.PRIMARY)
            checkbox_list.controls.append(cb)
        update_selected_count()
        page.update()

    def selecionar_jogador(e):
        jogador = e.control.data
        if e.control.value:
            if not any(s[0] == jogador[0] for s in selecionados):
                selecionados.append(jogador)
        else:
            selecionados[:] = [s for s in selecionados if s[0] != jogador[0]]
        update_selected_count()
        page.update()

    def update_selected_count():
         selected_count_text.value = f"Jogadores selecionados: {len(selecionados)}"
         page.update()

    def clear_selection(e):
        selecionados.clear()
        montar_lista_jogadores()
        page.update()

    async def share_teams(e, teams_data):
        text_to_copy = "Times Gerados:\n\n"
        for i, team in enumerate(teams_data):
            text_to_copy += f"Time {chr(65+i)} (Total Skill: {sum(j[2] for j in team)}):\n"
            for player in sorted(team, key=lambda x: x[1]):
                text_to_copy += f"- {player[1]} (Skill: {player[2]})\n"
            text_to_copy += "\n"
        
        await page.set_clipboard(text_to_copy)
        page.snack_bar = ft.SnackBar(ft.Text("Times copiados para a área de transferência!"), bgcolor=ft.colors.BLUE_700)
        page.snack_bar.open = True
        page.update()

    async def exibir_times(e):
        if not radio_times.value:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione o número de times"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
        if len(selecionados) < int(radio_times.value):
            page.snack_bar = ft.SnackBar(ft.Text("Jogadores insuficientes para o número de times selecionado."), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
        
        page.snack_bar = ft.SnackBar(ft.Text("Organizando times..."), bgcolor=ft.colors.BLUE_800)
        page.snack_bar.open = True
        
        page.opacity = 0
        page.update()
        await asyncio.sleep(0.1)

        resultado = organizar_times(selecionados, int(radio_times.value))
        col_times = []
        cores = ["#ee6002", "#021aee", "#41c300", "#C62828"]
        for i, time in enumerate(resultado):
            time_sorted = sorted(time, key=lambda x: x[1])
            jogadores_col = ft.Column([ft.Text(f"{j[1]} (Skill: {j[2]})", size=16, color=ft.colors.WHITE) for j in time_sorted])
            total = sum(j[2] for j in time)
            col_times.append(ft.Container(
                bgcolor=cores[i % len(cores)],
                border_radius=10,
                padding=10,
                content=ft.Column([
                    ft.Text(f"Time {chr(65 + i)}", weight="bold", color=ft.colors.WHITE, size=18),
                    jogadores_col,
                    ft.Divider(),
                    ft.Text(f"Total: {total}", size=14, weight="bold", color=ft.colors.WHITE)
                ])
            ))
        
        page.clean()
        page.add(
            ft.Row([ft.IconButton(icon="arrow_back", on_click=lambda event: page.run_task(voltar_para_selecao, event), icon_color=ft.colors.ON_SURFACE), ft.Text("Times Gerados", size=20, weight="bold"), theme_toggle_button]),
            ft.Row([
                ft.ElevatedButton("Reorganizar Times", on_click=lambda event: page.run_task(exibir_times, event)),
                ft.ElevatedButton("Compartilhar Times", on_click=lambda event: page.run_task(share_teams, event, resultado)),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Row(col_times, wrap=True, spacing=10, run_spacing=10, alignment="start")
        )
        page.snack_bar.open = False
        
        page.opacity = 1
        page.update()


    async def abrir_organizacao(e):
        montar_lista_jogadores()
        
        page.opacity = 0
        page.update()
        await asyncio.sleep(0.1)

        page.clean()
        page.add(
            ft.Column([
                ft.Row([ft.IconButton(icon="arrow_back", on_click=lambda event: page.run_task(voltar_home, event), icon_color=ft.colors.ON_SURFACE), ft.Text("Selecionar Jogadores", size=20), theme_toggle_button]),
                ft.Row([selected_count_text, ft.ElevatedButton("Limpar Seleção", on_click=clear_selection)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                checkbox_list,
                ft.Divider(),
                ft.Text("Número de Times:", size=16),
                radio_times,
                ft.ElevatedButton("Organizar", on_click=lambda event: page.run_task(exibir_times, event))
            ], scroll=ft.ScrollMode.ALWAYS)
        )
        page.opacity = 1
        page.update()

    async def voltar_home(e):
        page.opacity = 0
        page.update()
        await asyncio.sleep(0.1)

        page.clean()
        page.add(layout)
        
        page.opacity = 1
        page.update()

    async def voltar_para_selecao(e):
        page.opacity = 0
        page.update()
        await asyncio.sleep(0.1)

        page.clean()
        await abrir_organizacao(e)
        
    layout = ft.Column([
        ft.Container(
            content=ft.Text(
                "Organizador de Times",
                size=26,
                text_align="center",
                color=ft.colors.ON_SURFACE_VARIANT # Define a cor do texto explicitamente
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.SURFACE_VARIANT, # Altera a cor de fundo do container
            padding=20,
            border_radius=10
        ),
        ft.Row([
            ft.ElevatedButton("Organizar Times", icon=ft.icons.GROUP, on_click=lambda e: page.run_task(abrir_organizacao, e)),
            register_button,
            theme_toggle_button
        ], spacing=20, alignment=ft.MainAxisAlignment.SPACE_AROUND),
        input_container,
        ft.Container(content=mytable, alignment=ft.alignment.center, bgcolor=ft.colors.SURFACE, border_radius=20, padding=10)
    ], scroll=ft.ScrollMode.AUTO)

    page.add(layout)
    atualizar_tabela()

ft.app(target=main)