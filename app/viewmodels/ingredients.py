from typing import List, Dict, Any
from models.dishes import Ingredient, Dish
from repositories.ingredient_repository import IngredientRepository


class IngredientViewModel:
    def __init__(self, ingredient_repo: IngredientRepository):
        self.ingredient_repo = ingredient_repo
        self.ingredient: Ingredient | None = None
        self.dishes: List[Dish] = []

    def load_ingredient(self, ingredient_id: int) -> None:
        self.ingredient = self.ingredient_repo.find_one_or_none(ingredient_id)

    def get_dishes(self) -> List[Dish]:
        if not self.ingredient:
            raise ValueError('Ingredient not found')
        self.dishes = self.ingredient_repo.get_dishes(self.ingredient.id)
        return self.dishes

    def bulk_add(self, ingredient_names: List[str]) -> List[Ingredient]:
        return self.ingredient_repo.bulk_add_ingredients(ingredient_names)

    def to_dict(self) -> Dict[str, Any]:
        if not self.ingredient:
            return {}
        return {
            "id": self.ingredient.id,
            "name": self.ingredient.name,
            "dishes": [
                {
                    "id": d.id,
                    "name": d.name,
                    "description": d.description,
                    "image_url": d.image_url,
                }
                for d in self.dishes
            ],
        }
