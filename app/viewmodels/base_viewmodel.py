from typing import TypeVar, Generic, Dict, Any, List
from abc import ABC, abstractmethod


M = TypeVar("M")
R = TypeVar("R")


class BaseViewModel(Generic[M, R], ABC):
    def __init__(self, repository: R) -> None:
        self.repository = repository
        self.model: M | None = None
        self.related_data: List[Any] = []

    def add(self, model: M) -> None:
        if model:
            self.repository.add(model)
        else:
            raise ValueError(f"{self._get_model_name()} cannot be None")

    def load(self, model_id: int) -> None:
        self.model = self.repository.find_one_or_none(model_id)

    def delete(self) -> None:
        if not self.model:
            raise ValueError(f"{self._get_model_name()} not found")
        self.repository.delete(self.model)

    def update(self) -> None:
        if not self.model:
            raise ValueError(f"{self._get_model_name()} not found")

        data = dict(list(self.to_dict().items())[1:])
        self.repository.update(self.model.id, **data)

    def load_related_data(self) -> None:
        """Загрузка связанных данных (должен быть реализован в дочерних классах)"""
        if not self.model:
            raise ValueError(f"{self._get_model_name()} not found")
        self.related_data = self._load_related_data_impl()

    @abstractmethod
    def _load_related_data_impl(self) -> List[Any]:
        """Реализация загрузки связанных данных"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь (должен быть реализован в дочерних классах)"""
        pass

    def _get_model_name(self) -> str:
        """Получение имени модели для сообщений об ошибках"""
        return self.model.__class__.__name__ if self.model else "Model"
