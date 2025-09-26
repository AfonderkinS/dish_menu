import flet as ft

from models.database import init_db, get_session
from models.dishes import Cook, Dish
from repositories.cook_repository import CookRepository
from repositories.dish_repository import DishRepository
from repositories.ingredient_repository import IngredientRepository
from styles import PRIMARY_COLOR, ACCENT_COLOR
from viewmodels.cook_viewmodel import CookViewModel
from viewmodels.dish_viewmodel import DishListViewModel, DishViewModel
from viewmodels.ingredient_viewmodel import IngredientViewModel
from views.cook_detail_view import CookDetailView
from views.cook_list_view import CookListView
from views.dish_detail_view import DishDetailView
from views.dish_list_view import DishListView
from views.ingredient_detail_view import IngredientDetailView
from views.ingredient_list_view import IngredientListView


def main(page: ft.Page) -> None:
    page.title = "Популярные блюда"
    page.bgcolor = PRIMARY_COLOR
    page.scroll = ft.ScrollMode.AUTO
    page.theme = ft.Theme(color_scheme_seed=ACCENT_COLOR)

    init_db()
    session_factory = get_session

    cook_repo = CookRepository(session_factory)
    dish_repo = DishRepository(session_factory)
    ingredient_repo = IngredientRepository(session_factory)

    cook_vm = CookViewModel(cook_repo)
    dish_list_vm = DishListViewModel(dish_repo)
    dish_vm = DishViewModel(dish_repo)
    ingredient_vm = IngredientViewModel(ingredient_repo)

    content_area = ft.Container(expand=True)

    def show_cook_list():
        view = CookListView(
            page,
            cook_vm,
            on_select_cook=show_cook_detail,
        )
        view.load_data()
        content_area.content = view
        page.update()

    def show_cook_detail(cook_id: int):
        view = CookDetailView(
            page,
            cook_vm,
            cook_id,
            on_back=show_cook_list,
        )
        view.load_data()
        content_area.content = view
        page.update()

    def show_dish_list():
        view = DishListView(
            page, dish_list_vm, on_select_dish=show_dish_detail
        )
        view.load_data()
        content_area.content = view
        page.update()

    def show_dish_detail(dish_id: int):
        view = DishDetailView(
            page,
            dish_vm,
            dish_id,
            on_back=show_dish_list,
        )
        view.load_data()
        content_area.content = view
        page.update()

    def show_ingredient_list():
        view = IngredientListView(
            page, ingredient_vm, on_select_ingredient=show_ingredient_detail
        )
        view.load_data()
        content_area.content = view
        page.update()

    def show_ingredient_detail(ingredient_id: int):
        view = IngredientDetailView(
            page,
            ingredient_vm,
            ingredient_id,
            on_back=show_ingredient_list,
        )
        view.load_data()
        content_area.content = view
        page.update()

    navigation = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        expand=True,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Cooks"),
            ft.NavigationRailDestination(icon=ft.Icons.FOOD_BANK, label="Dishes"),
            ft.NavigationRailDestination(
                icon=ft.Icons.LOCAL_GROCERY_STORE, label="Ingredients"
            ),
        ],
        on_change=lambda e: {
            0: show_cook_list,
            1: show_dish_list,
            2: show_ingredient_list,
        }[e.control.selected_index](),
    )

    main_layout = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        navigation, width=200, bgcolor=PRIMARY_COLOR
                    ),  # Constrain width
                    ft.VerticalDivider(width=1),
                    content_area,
                ],
                expand=True,
                height=page.height,
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    page.controls.clear()
    page.controls.append(main_layout)
    page.update()
    show_cook_list()


if __name__ == "__main__":
    ft.app(target=main)
