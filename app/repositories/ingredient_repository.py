from typing import List
from models.dishes import Ingredient, dish_ingredient, Dish
from repositories.repository import BaseRepository


class IngredientRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory, Ingredient)

    def get_dishes(self, ingredient_id: int) -> List[Dish]:
        with self.session_factory() as session:
            query = (
                session.query(Dish)
                .join(dish_ingredient, Dish.id == dish_ingredient.c.dish_id)
                .filter(dish_ingredient.c.ingredient_id == ingredient_id)
            )
            return query.all()

    def bulk_add_ingredients(self, ingredients: list[str]) -> List[Ingredient]:
        with self.session_factory() as session:
            existing = session.query(self.model).filter(self.model.name.in_(ingredients)).all()
            existing_names = {ing.name for ing in existing}

            new_names = [name for name in ingredients if name not in existing_names]
            new_objects = [Ingredient(name=name) for name in new_names]

            if new_objects:
                session.add_all(new_objects)
                session.commit()
                existing.extend(new_objects)

            return existing
