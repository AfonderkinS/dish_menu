import flet as ft

from styles import (
    BODY_SIZE,
    CONTRAST_COLOR,
    SMALL_SIZE,
    SECONDARY_COLOR,
    get_text_style,
)


def create_list_item(title: str, subtitle: str = None, on_click=None, trailing=None):
    return ft.ListTile(
        title=ft.Text(title, style=get_text_style(BODY_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD)),
        subtitle=ft.Text(subtitle, style=get_text_style(SMALL_SIZE, SECONDARY_COLOR)) if subtitle else None,
        trailing=trailing,
        on_click=on_click
    )
