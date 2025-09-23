class BaseRepository:
    def __init__(self, session_factory, model):
        self.session_factory = session_factory
        self.model = model

    def find_all(self):
        with self.session_factory() as session:
            return session.query(self.model).all()

    def find_one_or_none(self, id: int):
        with self.session_factory() as session:
            return session.query(self.model).filter(self.model.id == id).one_or_none()

    def find_by_name(self, name: str):
        with self.session_factory() as session:
            return session.query(self.model).filter(self.model.name == name).first()

    def add(self, obj):
        with self.session_factory() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        return obj

    def update(self, obj, **kwargs):
        with self.session_factory() as session:
            obj = session.merge(obj)
            for field, value in kwargs.items():
                setattr(obj, field, value)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, obj):
        with self.session_factory() as session:
            obj = session.merge(obj)
            session.delete(obj)
            session.commit()

    def delete_by_id(self, id: int):
        with self.session_factory() as session:
            obj = session.query(self.model).filter(self.model.id == id).one_or_none()
            if obj:
                session.delete(obj)
                session.commit()
