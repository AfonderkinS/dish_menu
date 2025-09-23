from typing import List, Tuple

from sqlalchemy import func
from sqlalchemy.orm import aliased

from models.dishes import Cook, Dish
from repositories.repository import BaseRepository


class CookRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory, Cook)

    def get_top_cooks(self, limit: int) -> List[Tuple[Cook, int]]:
        with self.session_factory() as session:
            dish_alias = aliased(Dish)

            query = (
                session.query(
                    self.model,
                    func.count(dish_alias.id).label("dishes_count")
                ).outerjoin(dish_alias, self.model.id == dish_alias.cook_id)
                .group_by(self.model.id, self.model.name, self.model.bio)
                .order_by(func.count(dish_alias.id).desc())
                .limit(limit)
            )

            return query.all()

    def get_dishes_by_cook_id(self, cook_id) -> List[Dish]:
        with self.session_factory() as session:
            cook = session.query(self.model).filter(self.model.id == cook_id).one_or_none()
            if cook:
                return cook.dishes
            return []
