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
from viewmodels.ingredient_viewmodel import IngredientViewModel
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
    ):
        self._page = page
        self.view_model = view_model
        self.ingredient_id = ingredient_id
        self.on_back = on_back
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

    def _on_delete(self):
        self.view_model.delete_ingredient()

    def _on_update(self):
        self.view_model.update_ingredient()
        self.load_data()

    def load_data(self):
        self.view_model.load_ingredient(self.ingredient_id)
        if self.view_model.model:
            self.name_field.value = self.view_model.model.name
            self.view_model.get_dishes()
            self.dishes_list.controls.clear()
            for dish in self.view_model.dishes:
                self.dishes_list.controls.append(
                    create_list_item(title=dish.name, subtitle=dish.description)
                )
        self._page.update()

    def handle_update(self, e):
        if self.view_model.model:
            self.view_model.model.name = self.name_field.value
            self._on_update()

    def handle_delete(self, e):
        dialog = create_alert_dialog(
            "Confirm Delete",
            "Are you sure you want to delete this ingredient?",
            [
                create_button("Yes", on_click=lambda e: self.confirm_delete()),
                create_button("No", on_click=lambda e: self.close_dialog()),
            ],
        )
        self._page.open(dialog)
        self._page.update()

    def confirm_delete(self):
        if self.view_model.model:
            self._on_delete()
            self.on_back()
        self.close_dialog()

    def close_dialog(self):
        for control in self._page.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        self._page.update()
