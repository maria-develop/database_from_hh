import pytest

from src.hh_api import EmployerVacancyManager


@pytest.fixture
def employer_vacancy_manager():
    """Фикстура для инициализации класса EmployerVacancyManager."""
    return EmployerVacancyManager()
