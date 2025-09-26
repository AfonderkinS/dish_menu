from typing import List

import flet as ft


class FormBuilder:
    def __init__(self, title="Форма"):
        self.title = title
        self.fields = []
        self.on_save = None
        self.on_cancel = None

    def add_text_field(self, label: str, value: str = "", multiline=False, required=False):
        """Добавляет текстовое поле"""
        self.fields.append(
            {
                "type": "text",
                "label": label,
                "value": value,
                "multiline": multiline,
                "required": required,
            }
        )
        return self

    def add_dropdown(self, label: str, options: List[str], value=None, required=False):
        """Добавляет выпадающий список"""
        self.fields.append(
            {
                "type": "dropdown",
                "label": label,
                "options": options,
                "value": value,
                "required": required,
            }
        )
        return self

    def add_date_picker(self, label: str, value=None, required=False):
        """Добавляет поле выбора даты"""
        self.fields.append(
            {"type": "date", "label": label, "value": value, "required": required}
        )
        return self

    def add_checkbox(self, label: str, value=False):
        """Добавляет чекбокс"""
        self.fields.append({"type": "checkbox", "label": label, "value": value})
        return self

    def on_save_action(self, callback):
        """Устанавливает callback для кнопки Сохранить"""
        self.on_save = callback
        return self

    def on_cancel_action(self, callback):
        """Устанавливает callback для кнопки Отмена"""
        self.on_cancel = callback
        return self

    def build(self):
        """Создает и возвращает диалоговое окно с формой"""
        return FormDialog(self)


class FormDialog:
    def __init__(self, builder):
        self.builder = builder
        self.controls = []
        self.field_values = {}
        self.create_form()

    def create_form(self):
        """Создает элементы формы"""
        self.controls.clear()
        self.field_values.clear()

        for field in self.builder.fields:
            if field["type"] == "text":
                control = ft.TextField(
                    label=field["label"],
                    value=field["value"],
                    multiline=field.get("multiline", False),
                    on_change=self.on_field_change,
                )
                self.field_values[field["label"]] = control

            elif field["type"] == "dropdown":
                dropdown_options = [ft.dropdown.Option(opt) for opt in field["options"]]
                control = ft.Dropdown(
                    label=field["label"],
                    options=dropdown_options,
                    value=field["value"],
                    on_change=self.on_field_change,
                )
                self.field_values[field["label"]] = control

            elif field["type"] == "date":
                control = ft.TextField(
                    label=field["label"],
                    value=field["value"],
                    on_change=self.on_field_change,
                )
                self.field_values[field["label"]] = control

            elif field["type"] == "checkbox":
                control = ft.Checkbox(
                    label=field["label"],
                    value=field["value"],
                    on_change=self.on_field_change,
                )
                self.field_values[field["label"]] = control

            self.controls.append(control)

    def on_field_change(self, e):
        """Обработчик изменения полей"""
        pass

    def get_values(self):
        """Возвращает значения всех полей"""
        values = {}
        for label, control in self.field_values.items():
            if hasattr(control, "value"):
                values[label] = control.value
        return values

    def show(self, page):
        """Показывает диалоговое окно"""

        def save_clicked(e):
            if self.builder.on_save:
                self.builder.on_save(self.get_values())
            page.close(dialog)

        def cancel_clicked(e):
            if self.builder.on_cancel:
                self.builder.on_cancel()
            page.close(dialog)

        # Создаем диалоговое окно
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.builder.title),
            content=ft.Column(
                controls=self.controls, width=400, height=300, scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_clicked),
                ft.ElevatedButton("Сохранить", on_click=save_clicked),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)
        page.update()