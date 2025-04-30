import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Evita scaling automático
except:
    pass
import flet as ft
from flet import colors
import decimal as dec

botoes = [
    {'operador': 'AC', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100},
    {'operador': '+-', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100},
    {'operador': '%', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100},
    {'operador': '/', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '7', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '8', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '9', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '*', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '4', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '5', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '6', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '-', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '1', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '2', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '3', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '+', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '0', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '.', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '=', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
]
def main(page: ft.Page):
    page.bgcolor = colors.BLACK
    page.window_resizable = False
    page.window_width = 250
    page.window_height = 380
    page.title = "MB_Calc"
    page.window_always_on_top = True

    result = ft.Text(value="0", color=colors.WHITE, size=40)

    nova_operacao = False  # Variável de controle no escopo de main()

    def select(e):
        nonlocal nova_operacao

        value = e.control.content.value
        value_at = result.value if result.value != '0' else ''

        # Inicia nova operação após o "=" se um número for pressionado
        if nova_operacao and (value.isdigit() or value == '.'):
            result.value = value
            nova_operacao = False
        elif value == 'AC':
            result.value = '0'
            nova_operacao = False
        elif value == '+-':
            try:
                if result.value.startswith('-'):
                    result.value = result.value[1:]
                else:
                    result.value = '-' + result.value
            except Exception:
                result.value = '0'
            nova_operacao = False
        elif value == '=':
            try:
                expression = result.value.replace('%', '/100')
                resultado = eval(expression)
                resultado_decimal = dec.Decimal(str(resultado)).quantize(dec.Decimal('1.00000'))  # até 5 casas
                result.value = str(resultado_decimal).rstrip('0').rstrip('.')  # remove zeros/trailing ponto
            except Exception:
                result.value = 'Error'
            nova_operacao = True
        elif value.isdigit() or value == '.':
            result.value = (value_at + value) if result.value != '0' else value
            nova_operacao = False
        else:  # operador
            if not value_at or value_at[-1] in '+-*/%':
                result.value = value_at[:-1] + value
            else:
                result.value = value_at + value
            nova_operacao = False

        page.update()

    display = ft.Row(
        width=250,
        controls=[result],
        alignment = 'end',
    )

    btn = [ft.Container(
        content=ft.Text(value=btn['operador'], color=btn['fonte'], size=18),
        width=50,
        height=50,
        bgcolor=btn['fundo'],
        border_radius=100,
        alignment=ft.alignment.center,
        on_click=select
        ) for btn in botoes]

    keyboard = ft.Row(
        width=250,
        wrap=True,
        controls=btn,
        alignment='end'
    )

    page.add(display, keyboard)









ft.app(target=main)