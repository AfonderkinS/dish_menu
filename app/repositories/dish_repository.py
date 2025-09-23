from typing import List, Tuple

from sqlalchemy.orm import aliased

from models.dishes import Dish, Ingredient, dish_ingredient
from repositories.repository import BaseRepository


class DishRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory, Dish)

    def find_by_ingredient(self, ingredient_id: int) -> List[Dish]:
        with self.session_factory() as session:
            query = session.query(self.model).join(self.model.ingredients).filter(Ingredient.id == ingredient_id)
            return query.all()

    def add_or_update_ingredient(self, dish_id: int, ingredient_id: int, weight: float) -> Dish | None:
        with self.session_factory() as session:
            dish = session.query(self.model).filter(self.model.id == dish_id).one_or_none()
            ingredient = session.query(Ingredient).filter(Ingredient.id == ingredient_id).one_or_none()

            if not dish or not ingredient:
                return None

            existing = (
                session.query(dish_ingredient)
                .filter(
                    (dish_ingredient.c.dish_id == dish_id)
                    & (dish_ingredient.c.ingredient_id == ingredient_id)
                )
                .first()
            )

            if existing:
                session.execute(
                    dish_ingredient.update()
                    .where(
                        (dish_ingredient.c.dish_id == dish_id)
                        & (dish_ingredient.c.ingredient_id == ingredient_id)
                    )
                    .values(weight=weight)
                )
            else:
                session.execute(
                    dish_ingredient.insert().values(
                        dish_id=dish_id, ingredient_id=ingredient_id, weight=weight
                    )
                )

            session.commit()
            return dish

    def get_ingredients(self, dish_id: int) -> List[Tuple[Ingredient, float]]:
        with self.session_factory() as session:
            di_alias = aliased(dish_ingredient)
            query = session.query(
                Ingredient,
                di_alias.c.weight,
            ).join(di_alias).filter(di_alias.c.dish_id == dish_id)
            return query.all()
