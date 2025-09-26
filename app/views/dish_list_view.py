from typing import Callable

import flet as ft

from components.form_dialog import FormDialog, FormBuilder
from components.list_item import create_list_item
from models.dishes import Dish
from styles import (
    MARGIN,
    CONTRAST_COLOR,
    TITLE_SIZE,
    get_text_style,
    PADDING,
    PRIMARY_COLOR,
)
from viewmodels.dish_viewmodel import DishListViewModel
from components.button import create_button
from components.form_field import create_text_field


class DishListView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        view_model: DishListViewModel,
        on_select_dish: Callable,
    ):
        self._page = page
        self.view_model = view_model
        self.on_select_dish = on_select_dish
        self.search_field = create_text_field(
            "Search by name", on_change=self.handle_search
        )
        self.ingredient_filter = create_text_field(
            "Filter by ingredient ID", on_change=self.handle_filter
        )
        self.dishes_list = ft.ListView(expand=True, spacing=MARGIN)

        super().__init__(
            content=ft.Column(
                [
                    ft.Text(
                        "Dishes",
                        style=get_text_style(
                            TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD
                        ),
                    ),
                    self.search_field,
                    self.ingredient_filter,
                    self.dishes_list,
                    create_button(
                        "Add New Dish", on_click=lambda e: self._on_add_dish()
                    ),
                ],
                spacing=PADDING,
                expand=True,
            ),
            padding=PADDING,
            bgcolor=PRIMARY_COLOR,
        )

    def _on_add_dish(self):
        form: FormDialog = (
            FormBuilder("Add cook")
            .add_text_field("Name", required=True)
            .add_text_field("Description", required=True)
            .add_text_field("Recipe", required=True)
            .add_text_field("Image URL", required=True)
            .on_save_action(self._save_dish)
            .build()
        )
        form.show(self._page)

    def _save_dish(self, values):
        dish = Dish(
            name=values["Name"],
            description=values["Description"],
            recipe=values["Recipe"],
            image_url=values["Image URL"],
        )
        self.view_model.add_dish(dish)
        self.load_data()

    def load_data(self):
        self.view_model.load_all_dishes()
        self.update_list()

    def update_list(self):
        self.dishes_list.controls.clear()
        for dish in self.view_model.dishes:
            self.dishes_list.controls.append(
                create_list_item(
                    title=dish.name,
                    subtitle=dish.description,
                    on_click=lambda e, d=dish: self.on_select_dish(d.id)
                )
            )
        self._page.update()

    def handle_search(self, e):
        if self.search_field.value:
            self.view_model.search_by_name(self.search_field.value)
            self.update_list()
        else:
            self.load_data()
            self.update_list()

    def handle_filter(self, e):
        if self.ingredient_filter.value:
            try:
                ing_id = int(self.ingredient_filter.value)
                self.view_model.filter_by_ingredient(ing_id)
                self.update_list()
            except ValueError:
                pass
