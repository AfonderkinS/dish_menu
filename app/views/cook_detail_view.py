from typing import Callable

import flet as ft

from components.button import create_icon_button, create_button
from components.form_field import create_text_field
from components.list_item import create_list_item
from components.dialog import create_alert_dialog
from styles import MARGIN, get_text_style, TITLE_SIZE, CONTRAST_COLOR, SUBTITLE_SIZE, ERROR_COLOR, PADDING, \
    PRIMARY_COLOR
from viewmodels.cook_viewmodel import CookViewModel


class CookDetailView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        view_model: CookViewModel,
        cook_id: int, on_back: Callable,
    ):
        self._page = page
        self.view_model = view_model
        self.cook_id = cook_id
        self.on_back = on_back
        self.name_field = create_text_field("Name")
        self.bio_field = create_text_field("Bio", multiline=True)
        self.dishes_list = ft.ListView(expand=True, spacing=MARGIN)

        super().__init__(
            content=ft.Column([
                ft.Row([
                    create_icon_button(ft.Icons.ARROW_BACK, on_click=lambda e: self.on_back()),
                    ft.Text("Cook Details", style=get_text_style(TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD))
                ]),
                self.name_field,
                self.bio_field,
                ft.Text("Dishes", style=get_text_style(SUBTITLE_SIZE, CONTRAST_COLOR)),
                self.dishes_list,
                ft.Row([
                    create_button("Update", on_click=self.handle_update),
                    create_button("Delete", color=ERROR_COLOR, on_click=self.handle_delete)
                ])
            ], spacing=PADDING, expand=True),
            padding=PADDING,
            bgcolor=PRIMARY_COLOR
        )

    def _on_delete(self):
        self.view_model.delete_cook()

    def _on_update(self):
        self.view_model.update_cook()
        self.load_data()

    def load_data(self):
        self.view_model.load_cook(self.cook_id)
        self.view_model.load_dishes()
        if self.view_model.cook:
            self.name_field.value = self.view_model.cook.name
            self.bio_field.value = self.view_model.cook.bio
            self.dishes_list.controls.clear()
            for dish in self.view_model.dishes:
                self.dishes_list.controls.append(
                    create_list_item(title=dish.name, subtitle=dish.description)
                )
        self._page.update()

    def handle_update(self, e):
        if self.view_model.cook:
            self.view_model.cook.name = self.name_field.value
            self.view_model.cook.bio = self.bio_field.value
            self._on_update()

    def handle_delete(self, e):
        dialog = create_alert_dialog(
            "Confirm Delete",
            "Are you sure you want to delete this cook?",
            [
                create_button("Yes", on_click=lambda e: self.confirm_delete()),
                create_button("No", on_click=lambda e: self.close_dialog()),
            ],
        )
        self._page.open(dialog)
        self._page.update()

    def confirm_delete(self):
        if self.view_model.cook:
            self._on_delete()
            self.on_back()
        self.close_dialog()

    def close_dialog(self):
        for control in self._page.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        self._page.update()
