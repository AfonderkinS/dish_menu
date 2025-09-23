import flet as ft

from styles import (
    BORDER_RADIUS,
    TITLE_SIZE,
    CONTRAST_COLOR,
    SUBTITLE_SIZE,
    SECONDARY_COLOR,
    MARGIN,
    PADDING,
    get_text_style,
    get_card_style,
)


def create_card(
    content: ft.Control, title: str = None, subtitle: str = None, image_url: str = None
):
    children = []
    if image_url:
        children.append(
            ft.Image(
                src=image_url,
                fit=ft.ImageFit.COVER,
                width=200,
                height=150,
                border_radius=BORDER_RADIUS,
            )
        )
    if title:
        children.append(
            ft.Text(
                title,
                style=get_text_style(TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD),
            )
        )
    if subtitle:
        children.append(
            ft.Text(subtitle, style=get_text_style(SUBTITLE_SIZE, SECONDARY_COLOR))
        )
    children.append(content)

    return ft.Card(
        content=ft.Container(
            content=ft.Column(children, spacing=MARGIN),
            padding=PADDING,
            border_radius=BORDER_RADIUS,
        ),
        elevation=get_card_style()["elevation"],
        color=get_card_style()["color"],
        shape=get_card_style()["shape"],
    )
