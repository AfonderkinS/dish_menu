from typing import Callable

import flet as ft

from styles import (
    MARGIN,
    get_text_style,
    TITLE_SIZE,
    CONTRAST_COLOR,
    PADDING,
    PRIMARY_COLOR,
)
from viewmodels.ingredient_viewmodel import IngredientViewModel
from components.list_item import create_list_item
from components.button import create_button
from components.form_field import create_text_field


class IngredientListView(ft.Container):
    def __init__(self, page:ft.Page, view_model: IngredientViewModel, on_select_ingredient: Callable):
        self._page = page
        self.view_model = view_model
        self.on_select_ingredient = on_select_ingredient
        self.ingredients_list = ft.ListView(expand=True, spacing=MARGIN)
        self.bulk_add_field = create_text_field(
            "Bulk add names (comma-separated)", multiline=True
        )

        super().__init__(
            content=ft.Column(
                [
                    ft.Text(
                        "Ingredients",
                        style=get_text_style(
                            TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD
                        ),
                    ),
                    self.ingredients_list,
                    self.bulk_add_field,
                    create_button("Bulk Add", on_click=self.handle_bulk_add),
                ],
                spacing=PADDING,
                expand=True,
            ),
            padding=PADDING,
            bgcolor=PRIMARY_COLOR,
        )

    def load_data(self):
        ingredients = self.view_model.ingredient_repo.find_all()
        self.ingredients_list.controls.clear()
        for ing in ingredients:
            self.ingredients_list.controls.append(
                create_list_item(
                    title=ing.name,
                    on_click=lambda e, i=ing: self.on_select_ingredient(i.id),
                )
            )
        self._page.update()

    def handle_bulk_add(self, e):
        if self.bulk_add_field.value:
            names = [n.strip() for n in self.bulk_add_field.value.split(",")]
            self.view_model.bulk_add(names)
            self.bulk_add_field.value = ""
            self.load_data()
