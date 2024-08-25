from abc import ABC, abstractmethod
from typing import Any, List, Dict


class BaseEmployerVacancyManager(ABC):
    @abstractmethod
    def get_employers_by_name(self, name: str, per_page: int, page: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_vacancies_by_employer(self, employer_id: str, per_page: int, page: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def choose_employers(self) -> List[str]:
        pass

    @abstractmethod
    def get_vacancies_and_employer(self) -> List[Dict[str, Any]]:
        pass
