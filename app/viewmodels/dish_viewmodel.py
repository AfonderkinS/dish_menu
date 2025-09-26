from typing import List, Dict, Any

from models.dishes import Dish, Cook, Ingredient
from repositories.dish_repository import DishRepository


class DishViewModel:
    def __init__(self, dish_repo: DishRepository):
        self.dish_repo = dish_repo
        self.dish: Dish | None = None
        self.ingredients: List[Dict[str, Any]] = []
        self.available_cooks: List[Cook] = []
        self.available_ingredients: List[Ingredient] = []

    def delete_dish(self) -> None:
        self.dish_repo.delete(self.dish)

    def update_dish(self):
        id, data = self.dish.id, dict(list(self.to_dict().items())[1:])
        self.dish_repo.update(id, **data)

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

    def get_available_cooks(self) -> List[Cook]:
        self.available_cooks = self.dish_repo.get_available_cooks()
        return self.available_cooks

    def get_available_ingredients(self) -> List[Ingredient]:
        self.available_ingredients = self.dish_repo.get_available_ingredients()
        return self.available_ingredients

    def set_dish_cook(self, cook_id: int) -> None:
        if not self.dish:
            raise ValueError("dish not found")
        self.dish_repo.set_dish_cook(self.dish.id, cook_id)
        self.load_dish(self.dish.id)

    def to_dict(self) -> Dict[str, Any]:
        if not self.dish:
            return {}
        if not self.ingredients:
            self.get_ingredients()
        return {
            "id": self.dish.id,
            "name": self.dish.name,
            "recipe": self.dish.recipe,
            "description": self.dish.description,
            "image_url": self.dish.image_url,
            "ingredients": self.ingredients,
        }


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
