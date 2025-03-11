from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class DBManagerABC(ABC):
    """Абстрактный базовый класс для менеджера базы данных"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> List[Tuple[Any, ...]]:
        pass

    @abstractmethod
    def get_all_vacancies(self) -> List[Tuple[Any, ...]]:
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> List[Tuple[Any, ...]]:
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[Any, ...]]:
        pass
