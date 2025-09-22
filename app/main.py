import flet as ft


def main(page: ft.Page) -> None:
    page.title = "Популярные блюда"
    page.bgcolor = "black"
    page.scroll = "auto"

    page.update()


if __name__ == "__main__":
    ft.app(target=main)