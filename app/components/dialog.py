import flet as ft

from styles import TITLE_SIZE, BODY_SIZE, CONTRAST_COLOR, get_text_style


def create_alert_dialog(title: str, content: str, actions: list[ft.Control]):
    return ft.AlertDialog(
        title=ft.Text(title, style=get_text_style(TITLE_SIZE, CONTRAST_COLOR)),
        content=ft.Text(content, style=get_text_style(BODY_SIZE, CONTRAST_COLOR)),
        actions=actions,
    )
