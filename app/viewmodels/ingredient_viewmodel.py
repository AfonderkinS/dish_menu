from typing import List, Dict, Any

from models.dishes import Ingredient, Dish
from repositories.ingredient_repository import IngredientRepository
from viewmodels.base_viewmodel import BaseViewModel


class IngredientViewModel(BaseViewModel[Ingredient, IngredientRepository]):
    def __init__(self, ingredient_repo: IngredientRepository):
        super().__init__(ingredient_repo)
        self.dishes: List[Dish] = []

    def _load_related_data_impl(self) -> List[Dish]:
        """Загрузка блюд, содержащих ингредиент"""
        if not self.model:
            return []

        self.dishes = self.repository.get_dishes(self.model.id)
        return self.dishes

    def get_dishes(self) -> List[Dish]:
        """Получение блюд с ингредиентом"""
        self.load_related_data()
        return self.dishes

    def bulk_add(self, ingredient_names: List[str]) -> List[Ingredient]:
        return self.repository.bulk_add_ingredients(ingredient_names)

    def to_dict(self) -> Dict[str, Any]:
        if not self.model:
            return {}

        if not self.dishes:
            self.load_related_data()

        return {
            "id": self.model.id,
            "name": self.model.name,
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

    # Алиасы для обратной совместимости
    def load_ingredient(self, ingredient_id: int) -> None:
        self.load(ingredient_id)

    def delete_ingredient(self) -> None:
        self.delete()

    def update_ingredient(self) -> None:
        self.update()
