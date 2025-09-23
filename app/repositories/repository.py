from typing import TypeVar, List


MT = TypeVar("MT")


class BaseRepository:
    def __init__(self, session_factory, model: MT):
        self.session_factory = session_factory
        self.model = model

    def find_all(self) -> List[MT]:
        with self.session_factory() as session:
            return session.query(self.model).all()

    def find_one_or_none(self, id: int) -> MT | None:
        with self.session_factory() as session:
            return session.query(self.model).filter(self.model.id == id).one_or_none()

    def find_by_name(self, name: str) -> MT | None:
        with self.session_factory() as session:
            return session.query(self.model).filter(self.model.name.ilike(f"%{name}%")).first()

    def add(self, obj: MT) -> MT:
        with self.session_factory() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        return obj

    def update(self, obj: MT, **kwargs) -> MT:
        with self.session_factory() as session:
            obj = session.merge(obj)
            for field, value in kwargs.items():
                setattr(obj, field, value)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, obj: MT) -> None:
        with self.session_factory() as session:
            obj = session.merge(obj)
            session.delete(obj)
            session.commit()

    def delete_by_id(self, id: int) -> None:
        with self.session_factory() as session:
            obj = session.query(self.model).filter(self.model.id == id).one_or_none()
            if obj:
                session.delete(obj)
                session.commit()
