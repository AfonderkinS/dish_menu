from typing import List, Dict, Any

from models.dishes import Dish
from repositories.dish_repository import DishRepository


class DishViewModel:
    def __init__(self, dish_repo: DishRepository):
        self.dish_repo = dish_repo
        self.dish: Dish | None = None
        self.ingredients: List[Dict[str, Any]] = []

    def load_dish(self, dish_id: int) -> None:
        self.dish = self.dish_repo.find_one_or_none(id=dish_id)

    def get_ingredients(self) -> List[Dict[str, Any]]:
        if not self.dish:
            raise ValueError("dish not found")
        raw_ingredients = self.dish_repo.get_ingredients(self.dish.id)
        self.ingredients = [
            {"id": ing.id, "name": ing.name, "weight": weight}
            for ing, weight in raw_ingredients
        ]
        return self.ingredients

    def add_or_update_ingredient(self, ingredient_id: int, weight: float) -> None:
        if not self.dish:
            raise ValueError("dish not found")
        self.dish = self.dish_repo.add_or_update_ingredient(self.dish.id, ingredient_id, weight)

    def delete_ingredient(self, ingredient_id: int) -> None:
        if not self.dish:
            raise ValueError("dish not found")
        self.dish_repo.remove_ingredient(self.dish.id, ingredient_id)
        self.ingredients = self.get_ingredients()


class DishListViewModel:
    def __init__(self, dish_repo: DishRepository):
        self.dish_repo = dish_repo
        self.dishes: List[Dish] = []
        self.selected_ingredient: int | None = None

    def load_all_dishes(self) -> None:
        self.dishes = self.dish_repo.find_all()

    def filter_by_ingredient(self, ingredient_id: int) -> None:
        self.dishes = self.dish_repo.find_by_ingredient(ingredient_id)

    def search_by_name(self, name: str) -> None:
        self.dishes = self.dish_repo.find_by_name(name)
