from sqlalchemy import Table, Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from models.database import Base


dish_ingredient = Table(
    "dish_ingredients",
    Base.metadata,
    Column("dish_id", Integer, ForeignKey("dishes.id", ondelete="RESTRICT"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id", ondelete="RESTRICT"), primary_key=True),
    Column("weight", Float, default=0.0)
)


class Cook(Base):
    __tablename__ = "cooks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=False, default="")

    dishes = relationship("Dish", back_populates="cook")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    recipe = Column(String, nullable=False, default="")
    image_url = Column(String, nullable=True)
    cook_id = Column(Integer, ForeignKey("cooks.id", ondelete="CASCADE"))

    cook = relationship("Cook", back_populates="dishes")
    ingredients = relationship(
        "Ingredient",
        secondary=dish_ingredient,
        back_populates="dishes"
    )


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    dishes = relationship(
        "Dish",
        secondary=dish_ingredient,
        back_populates="ingredients"
    )