import flet as ft

from styles import (
    BODY_SIZE,
    CONTRAST_COLOR,
    SMALL_SIZE,
    SECONDARY_COLOR,
    ACCENT_COLOR,
    get_text_style,
)


def create_text_field(
    label: str, value: str = None, on_change=None, multiline: bool = False
):
    return ft.TextField(
        label=label,
        value=value,
        multiline=multiline,
        text_style=get_text_style(BODY_SIZE, CONTRAST_COLOR),
        label_style=get_text_style(SMALL_SIZE, SECONDARY_COLOR),
        border_color=SECONDARY_COLOR,
        focused_border_color=ACCENT_COLOR,
        on_change=on_change,
    )


def create_number_field(label: str, value: float = None, on_change=None):
    return ft.TextField(
        label=label,
        value=str(value) if value is not None else None,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=get_text_style(BODY_SIZE, CONTRAST_COLOR),
        label_style=get_text_style(SMALL_SIZE, SECONDARY_COLOR),
        border_color=SECONDARY_COLOR,
        focused_border_color=ACCENT_COLOR,
        on_change=on_change,
    )
