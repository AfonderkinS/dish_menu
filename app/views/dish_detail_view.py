from typing import Callable

import flet as ft

from styles import (
    MARGIN,
    TITLE_SIZE,
    CONTRAST_COLOR,
    get_text_style,
    SUBTITLE_SIZE,
    ERROR_COLOR,
    PADDING,
    PRIMARY_COLOR,
)
from viewmodels.dish_viewmodel import DishViewModel
from components.form_field import create_text_field, create_number_field
from components.button import create_button, create_icon_button
from components.list_item import create_list_item
from components.dialog import create_alert_dialog


class DishDetailView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        view_model: DishViewModel,
        dish_id: int,
        on_back: Callable,
    ):
        self._page = page
        self.view_model = view_model
        self.dish_id = dish_id
        self.on_back = on_back
        self.name_field = create_text_field("Name")
        self.description_field = create_text_field("Description", multiline=True)
        self.recipe_field = create_text_field("Recipe", multiline=True)
        self.image_url_field = create_text_field("Image URL")
        self.cook_dropdown = ft.Dropdown(
            label="Cook",
            options=[],
            expand=True,
            on_change=self.handle_cook_change,
            color=CONTRAST_COLOR,
        )
        self.ingredients_list = ft.ListView(expand=True, spacing=MARGIN)
        self.ingredient_dropdown = ft.Dropdown(
            label="Ingredient",
            options=[],
            expand=True,
            color=CONTRAST_COLOR,
        )
        self.new_weight = create_number_field("Weight")

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            create_icon_button(
                                ft.Icons.ARROW_BACK, on_click=lambda e: self.on_back()
                            ),
                            ft.Text(
                                "Dish Details",
                                style=get_text_style(
                                    TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD
                                ),
                            ),
                        ]
                    ),
                    self.name_field,
                    self.description_field,
                    self.recipe_field,
                    self.image_url_field,
                    ft.Row([self.cook_dropdown]),
                    ft.Text(
                        "Ingredients",
                        style=get_text_style(SUBTITLE_SIZE, CONTRAST_COLOR),
                    ),
                    self.ingredients_list,
                    ft.Row(
                        [
                            self.ingredient_dropdown,
                            self.new_weight,
                            create_button(
                                "Add/Update Ingredient",
                                on_click=self.handle_add_ingredient,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            create_button("Update Dish", on_click=self.handle_update),
                            create_button(
                                "Delete Dish",
                                color=ERROR_COLOR,
                                on_click=self.handle_delete,
                            ),
                        ]
                    ),
                ],
                spacing=PADDING,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=PADDING,
            bgcolor=PRIMARY_COLOR,
        )

    def _on_delete(self):
        self.view_model.delete_dish()

    def _on_update(self):
        self.view_model.update_dish()
        self.load_data()

    def load_data(self):
        self.view_model.load_dish(self.dish_id)
        if self.view_model.model:
            self.name_field.value = self.view_model.model.name
            self.description_field.value = self.view_model.model.description
            self.recipe_field.value = self.view_model.model.recipe
            self.image_url_field.value = self.view_model.model.image_url

            self.load_ingredients()
            self.load_cooks()
            self.update_ingredients()

    def load_ingredients(self):
        ingredients = self.view_model.get_available_ingredients()
        self.ingredient_dropdown.options.clear()
        self.ingredient_dropdown.options.append(
            ft.dropdown.Option(key="", text="Select ingredient")
        )
        for ingredient in ingredients:
            self.ingredient_dropdown.options.append(
                ft.dropdown.Option(key=str(ingredient.id), text=ingredient.name)
            )
        self.ingredient_dropdown.value = ""

    def load_cooks(self):
        cooks = self.view_model.get_available_cooks()
        self.cook_dropdown.options.clear()
        for cook in cooks:
            self.cook_dropdown.options.append(
                ft.dropdown.Option(key=str(cook.id), text=cook.name)
            )
        if self.view_model.model and self.view_model.model.cook_id:
            self.cook_dropdown.value = str(self.view_model.model.cook_id)
        else:
            self.cook_dropdown.value = ""

    def update_ingredients(self):
        self.ingredients_list.controls.clear()
        ingredients = self.view_model.get_ingredients()
        for ing in ingredients:
            self.ingredients_list.controls.append(
                create_list_item(
                    title=ing["name"],
                    subtitle=f"Weight: {ing['weight']}",
                    trailing=create_icon_button(
                        ft.Icons.DELETE,
                        on_click=lambda e, i=ing["id"]: self.handle_remove_ingredient(
                            i
                        ),
                    ),
                )
            )
        self._page.update()

    def handle_cook_change(self, e):
        if e.control.value and e.control.value != "":
            cook_id = int(e.control.value)
            self.view_model.set_dish_cook(cook_id)
            self.load_data()

    def handle_add_ingredient(self, e):
        try:
            if (
                not self.ingredient_dropdown.value
                or self.ingredient_dropdown.value == ""
            ):
                return

            ing_id = int(self.ingredient_dropdown.value)
            weight = float(self.new_weight.value)
            self.view_model.add_or_update_ingredient(ing_id, weight)
            self.update_ingredients()
            self.ingredient_dropdown.value = ""
            self.new_weight.value = ""
            self._page.update()
        except ValueError:
            pass

    def handle_remove_ingredient(self, ingredient_id: int):
        self.view_model.delete_ingredient(ingredient_id)
        self.update_ingredients()

    def handle_update(self, e):
        if self.view_model.model:
            self.view_model.model.name = self.name_field.value
            self.view_model.model.description = self.description_field.value
            self.view_model.model.recipe = self.recipe_field.value
            self.view_model.model.image_url = self.image_url_field.value
            self._on_update()

    def handle_delete(self, e):
        dialog = create_alert_dialog(
            "Confirm Delete",
            "Are you sure you want to delete this dish?",
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
