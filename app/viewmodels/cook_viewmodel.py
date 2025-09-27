from typing import List, Dict, Any
from models.dishes import Cook, Dish
from repositories.cook_repository import CookRepository
from viewmodels.base_viewmodel import BaseViewModel


class CookViewModel(BaseViewModel[Cook, CookRepository]):
    def __init__(self, cook_repo: CookRepository):
        super().__init__(cook_repo)
        self.dishes: List[Dish] = []

    def _load_related_data_impl(self) -> List[Dish]:
        """Загрузка блюд повара"""
        self.dishes = self.repository.get_dishes_by_cook_id(cook_id=self.model.id)
        return self.dishes

    def load_dishes(self) -> None:
        """Алиас для обратной совместимости"""
        self.load_related_data()

    def get_top_cooks(self, limit: int) -> List[Dict[str, Any]]:
        raw_results = self.repository.get_top_cooks(limit)
        return [
            {
                "id": cook.id,
                "name": cook.name,
                "bio": cook.bio,
                "dishes_count": dishes_count,
            }
            for cook, dishes_count in raw_results
        ]

    def to_dict(self) -> Dict[str, Any]:
        if not self.model:
            return {}

        if not self.dishes:
            self.load_related_data()

        return {
            "id": self.model.id,
            "name": self.model.name,
            "bio": self.model.bio,
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
    def add_cook(self, cook: Cook) -> None:
        self.add(cook)

    def load_cook(self, cook_id: int) -> None:
        self.load(cook_id)

    def delete_cook(self) -> None:
        self.delete()

    def update_cook(self) -> None:
        self.update()
