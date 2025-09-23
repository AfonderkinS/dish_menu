from typing import Callable

import flet as ft

from styles import (
    MARGIN,
    get_text_style,
    TITLE_SIZE,
    CONTRAST_COLOR,
    SUBTITLE_SIZE,
    ERROR_COLOR,
    PADDING,
    PRIMARY_COLOR,
)
from viewmodels.ingredients import IngredientViewModel
from components.form_field import create_text_field
from components.button import create_button, create_icon_button
from components.list_item import create_list_item
from components.dialog import create_alert_dialog


class IngredientDetailView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        view_model: IngredientViewModel,
        ingredient_id: int,
        on_back: Callable,
        on_update: Callable,
        on_delete: Callable,
    ):
        self._page = page
        self.view_model = view_model
        self.ingredient_id = ingredient_id
        self.on_back = on_back
        self.on_update = on_update
        self.on_delete = on_delete
        self.name_field = create_text_field("Name")
        self.dishes_list = ft.ListView(expand=True, spacing=MARGIN)

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            create_icon_button(
                                ft.Icons.ARROW_BACK, on_click=lambda e: self.on_back()
                            ),
                            ft.Text(
                                "Ingredient Details",
                                style=get_text_style(
                                    TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD
                                ),
                            ),
                        ]
                    ),
                    self.name_field,
                    ft.Text(
                        "Dishes", style=get_text_style(SUBTITLE_SIZE, CONTRAST_COLOR)
                    ),
                    self.dishes_list,
                    ft.Row(
                        [
                            create_button("Update", on_click=self.handle_update),
                            create_button(
                                "Delete",
                                color=ERROR_COLOR,
                                on_click=self.handle_delete,
                            ),
                        ]
                    ),
                ],
                spacing=PADDING,
                expand=True,
            ),
            padding=PADDING,
            bgcolor=PRIMARY_COLOR,
        )

    def load_data(self):
        self.view_model.load_ingredient(self.ingredient_id)
        if self.view_model.ingredient:
            self.name_field.value = self.view_model.ingredient.name
            self.view_model.get_dishes()
            self.dishes_list.controls.clear()
            for dish in self.view_model.dishes:
                self.dishes_list.controls.append(
                    create_list_item(title=dish.name, subtitle=dish.description)
                )
        self._page.update()

    def handle_update(self, e):
        if self.view_model.ingredient:
            self.view_model.ingredient.name = self.name_field.value
            self.on_update(self.view_model.ingredient)

    def handle_delete(self, e):
        dialog = create_alert_dialog(
            "Confirm Delete",
            "Are you sure you want to delete this ingredient?",
            [
                create_button("Yes", on_click=lambda e: self.confirm_delete()),
                create_button("No", on_click=lambda e: self.close_dialog()),
            ],
        )
        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()

    def confirm_delete(self):
        if self.view_model.ingredient:
            self.on_delete(self.view_model.ingredient)
        self.close_dialog()

    def close_dialog(self):
        for control in self._page.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        self._page.update()
