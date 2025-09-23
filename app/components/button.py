import flet as ft

from styles import ACCENT_COLOR, PRIMARY_COLOR, get_button_style, CONTRAST_COLOR


def create_button(text: str, on_click=None, color: str = ACCENT_COLOR, text_color: str = PRIMARY_COLOR):
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        style=get_button_style(color, text_color)
    )

def create_icon_button(icon: str, on_click=None, tooltip: str = None):
    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        on_click=on_click,
        icon_color=CONTRAST_COLOR
    )
