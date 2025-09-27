from typing import List, Dict, Any

from models.dishes import Dish, Cook, Ingredient
from repositories.dish_repository import DishRepository
from viewmodels.base_viewmodel import BaseViewModel


class DishViewModel(BaseViewModel[Dish, DishRepository]):
    def __init__(self, dish_repo: DishRepository):
        super().__init__(dish_repo)
        self.ingredients: List[Dict[str, Any]] = []
        self.available_cooks: List[Cook] = []
        self.available_ingredients: List[Ingredient] = []

    def _load_related_data_impl(self) -> List[Dict[str, Any]]:
        """Загрузка ингредиентов блюда"""
        if not self.model:
            return []

        raw_ingredients = self.repository.get_ingredients(self.model.id)
        self.ingredients = [
            {"id": ing.id, "name": ing.name, "weight": weight}
            for ing, weight in raw_ingredients
        ]
        return self.ingredients

    def get_ingredients(self) -> List[Dict[str, Any]]:
        """Получение ингредиентов блюда"""
        self.load_related_data()
        return self.ingredients

    def add_or_update_ingredient(self, ingredient_id: int, weight: float) -> None:
        if not self.model:
            raise ValueError("Dish not found")
        self.model = self.repository.add_or_update_ingredient(
            self.model.id, ingredient_id, weight
        )
        self.load_related_data()

    def delete_ingredient(self, ingredient_id: int) -> None:
        if not self.model:
            raise ValueError("Dish not found")
        self.repository.remove_ingredient(self.model.id, ingredient_id)
        self.load_related_data()

    def get_available_cooks(self) -> List[Cook]:
        self.available_cooks = self.repository.get_available_cooks()
        return self.available_cooks

    def get_available_ingredients(self) -> List[Ingredient]:
        self.available_ingredients = self.repository.get_available_ingredients()
        return self.available_ingredients

    def set_dish_cook(self, cook_id: int) -> None:
        if not self.model:
            raise ValueError("Dish not found")
        self.repository.set_dish_cook(self.model.id, cook_id)
        self.load(self.model.id)

    def to_dict(self) -> Dict[str, Any]:
        if not self.model:
            return {}

        if not self.ingredients:
            self.load_related_data()

        return {
            "id": self.model.id,
            "name": self.model.name,
            "recipe": self.model.recipe,
            "description": self.model.description,
            "image_url": self.model.image_url,
            "ingredients": self.ingredients,
        }

    def delete_dish(self) -> None:
        self.delete()

    def update_dish(self) -> None:
        self.update()

    def load_dish(self, dish_id: int) -> None:
        self.load(dish_id)


class DishListViewModel:
    def __init__(self, dish_repo: DishRepository):
        self.dish_repo = dish_repo
        self.dishes: List[Dish] = []
        self.selected_ingredient: int | None = None

    def add_dish(self, dish: Dish) -> None:
        if dish:
            self.dish_repo.add(dish)
        else:
            raise ValueError("Dish cannot be None")

    def load_all_dishes(self) -> None:
        self.dishes = self.dish_repo.find_all()

    def filter_by_ingredient(self, ingredient_id: int) -> None:
        self.selected_ingredient = ingredient_id
        self.dishes = self.dish_repo.find_by_ingredient(ingredient_id)

    def search_by_name(self, name: str) -> None:
        self.dishes = self.dish_repo.find_by_name(name)

    def to_dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": dish.id,
                "name": dish.name,
                "description": dish.description,
                "image_url": dish.image_url,
                "recipe": dish.recipe,
            }
            for dish in self.dishes
        ]
