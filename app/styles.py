import flet as ft


PRIMARY_COLOR = ft.Colors.WHITE
CONTRAST_COLOR = ft.Colors.BLACK
ACCENT_COLOR = ft.Colors.BLUE_700
SECONDARY_COLOR = ft.Colors.GREY_800
ERROR_COLOR = ft.Colors.RED_700
SUCCESS_COLOR = ft.Colors.GREEN_700

FONT_FAMILY = "Roboto"
TITLE_SIZE = 24
SUBTITLE_SIZE = 18
BODY_SIZE = 14
SMALL_SIZE = 12

PADDING = 16
MARGIN = 8
BORDER_RADIUS = 8

def get_text_style(size: int = BODY_SIZE, color: str = CONTRAST_COLOR, weight: ft.FontWeight = ft.FontWeight.NORMAL):
    return ft.TextStyle(
        font_family=FONT_FAMILY,
        size=size,
        color=color,
        weight=weight
    )

def get_button_style(bgcolor: str = ACCENT_COLOR, color: str = PRIMARY_COLOR):
    return ft.ButtonStyle(
        bgcolor=bgcolor,
        color=color,
        shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
    )

def get_card_style(elevation: float = 2):
    return {
        "elevation": elevation,
        "color": PRIMARY_COLOR,
        "shape": ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
    }
