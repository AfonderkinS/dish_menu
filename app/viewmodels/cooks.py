from typing import List, Dict, Any
from models.dishes import Cook, Dish
from repositories.cook_repository import CookRepository


class CookViewModel:
    def __init__(self, cook_repo: CookRepository):
        self.cook_repo = cook_repo
        self.cook: Cook | None = None
        self.dishes: List[Dish] = []

    def load_cook(self, cook_id: int) -> None:
        self.cook = self.cook_repo.find_one_or_none(cook_id)

    def load_dishes(self) -> None:
        if not self.cook:
            raise ValueError("Cook not found")
        self.dishes = self.cook_repo.get_dishes_by_cook_id(cook_id=self.cook.id)

    def get_top_cooks(self, limit: int) -> List[Dict[str, Any]]:
        raw_results = self.cook_repo.get_top_cooks(limit)
        return [
            {
                "id": cook.id,
                "name": cook.name,
                "bio": cook.bio,
                "dishes_count": dishes_count,
            }
            for cook, dishes_count in raw_results
        ]
