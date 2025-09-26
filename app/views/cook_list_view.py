from typing import Callable

import flet as ft

from components.button import create_button
from components.card import create_card
from components.list_item import create_list_item
from components.form_dialog import FormBuilder, FormDialog
from models.dishes import Cook
from styles import (
    MARGIN,
    get_text_style,
    TITLE_SIZE,
    CONTRAST_COLOR,
    PADDING,
    PRIMARY_COLOR,
    BODY_SIZE,
    SECONDARY_COLOR,
)
from viewmodels.cook_viewmodel import CookViewModel


class CookListView(ft.Container):
    def __init__(
        self, page: ft.Page, view_model: CookViewModel, on_select_cook: Callable
    ):
        self._page = page
        self.view_model = view_model
        self.on_select_cook = on_select_cook
        self.top_cooks_list = ft.ListView(expand=True, spacing=MARGIN)
        self.all_cooks_list = ft.ListView(expand=True, spacing=MARGIN)

        super().__init__(
            content=ft.Column(
                [
                    ft.Text(
                        "Top Cooks",
                        style=get_text_style(
                            TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD
                        ),
                    ),
                    self.top_cooks_list,
                    ft.Text(
                        "All Cooks",
                        style=get_text_style(
                            TITLE_SIZE, CONTRAST_COLOR, ft.FontWeight.BOLD
                        ),
                    ),
                    self.all_cooks_list,
                    create_button(
                        "Add New Cook", on_click=lambda e: self._on_add_cook()
                    ),
                ],
                spacing=PADDING,
                expand=True,
            ),
            padding=PADDING,
            bgcolor=PRIMARY_COLOR,
        )

    def _on_add_cook(self):
        form: FormDialog = (
            FormBuilder("Add cook")
            .add_text_field("Name", required=True)
            .add_text_field("Bio", required=True)
            .on_save_action(self._save_cook)
            .build()
        )
        form.show(self._page)

    def _save_cook(self, values):
        cook = Cook(
            name=values["Name"],
            bio=values["Bio"],
        )
        self.view_model.add_cook(cook)
        self.load_data()

    def load_data(self):
        self.top_cooks_list.controls.clear()
        top_cooks = self.view_model.get_top_cooks(5)
        for cook in top_cooks:
            self.top_cooks_list.controls.append(
                create_card(
                    ft.Text(
                        f"Dishes: {cook['dishes_count']}",
                        style=get_text_style(BODY_SIZE, SECONDARY_COLOR),
                    ),
                    title=cook["name"],
                    subtitle=cook["bio"],
                )
            )

        self.all_cooks_list.controls.clear()
        all_cooks = self.view_model.cook_repo.find_all()
        for cook in all_cooks:
            self.all_cooks_list.controls.append(
                create_list_item(
                    title=cook.name,
                    subtitle=cook.bio,
                    on_click=lambda e, c=cook: self.on_select_cook(c.id),
                )
            )
        self._page.update()
