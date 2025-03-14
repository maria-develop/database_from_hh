import requests

from typing import Any
from src.hh_api_abstract import BaseEmployerVacancyManager


class EmployerVacancyManager(BaseEmployerVacancyManager):
    """Класс для работы с данными работодателей и вакансий через API hh.ru."""
    def get_employers_by_name(self, name: str, per_page: int = 20, page: int = 0) -> list[dict[str, Any]]:
        """
        Функция для получения списка работодателей по имени с hh.ru.
        :param name: Имя работодателя для поиска.
        :param per_page: Количество работодателей на одной странице (по умолчанию 20).
        :param page: Номер страницы для поиска (по умолчанию 0).
        :return: Список работодателей.
        """
        url = "https://api.hh.ru/employers"
        params = {
            "text": name,
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        employers_data = response.json()
        # print(employers_data.get("items", []))
        return employers_data.get("items", [])

    def get_vacancies_by_employer(self, employer_id: str, per_page: int = 20, page: int = 0) -> list[dict[str, Any]]:
        """
        Функция для получения списка вакансий работодателя с hh.ru.
        :param employer_id: ID работодателя.
        :param per_page: Количество вакансий на одной странице (по умолчанию 20).
        :param page: Номер страницы для поиска (по умолчанию 0).
        :return: Список вакансий.
        """
        url = "https://api.hh.ru/vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancies_data = response.json()

        return vacancies_data.get("items", [])

    def choose_employers(self) -> list[str]:
        """
        Функция для запроса у пользователя списка из 10 работодателей для поиска вакансий.
        :return: Список имен работодателей.
        """
        employers = []
        print("Введите 10 имен работодателей, чтобы найти их вакансии на hh.ru: ")
        for i in range(10):
            name = input(f"{i + 1}. Имя работодателя: ").strip()
            employers.append(name)
        return employers

    def get_vacancies_and_employer(self) -> list[dict[str, Any]]:
        """
            Получает информацию о работодателях и их вакансиях.
            :return: Список словарей с информацией о работодателях и вакансиях.
        """
        # all_employers = []
        # all_vacancies = []
        employer_with_vacancies_list = []

        # Запрашиваем у пользователя 10 работодателей
        # employer_names = choose_employers()
        # Передаем список 10 работодателей
        employer_names = [
            'ООО Транснефть Финанс',
            'Футбольный клуб Рубин',
            'АО ИСК Тандем',
            'Казанская Ривьера-Отель',
            'ООО Юнисервис',
            'ООО Жар Свежар',
            'АО Транснефть - Прикамье',
            'МКУ Комитет жилищно-коммунального хозяйства города Казани',
            'Казанский авиационный завод им. С.П. Горбунова - филиал АО Туполев',
            'ООО Транснефть-Синтез'
        ]

        # Для каждого работодателя получаем список вакансий
        for employer_name in employer_names:
            employers = self.get_employers_by_name(employer_name)

            if not employers:
                print(f"Работодатель с именем '{employer_name}' не найден.")
                return []
                # continue

            for employer in employers:
                employer_data = {
                    "employer_name": employer['name'],
                    "id": employer['id'],
                    "alternate_url": employer['alternate_url'],
                    "open_vacancies": employer['open_vacancies']
                    # "vacancies": []
                }
                vacancies_info = []

                vacancies = self.get_vacancies_by_employer(employer['id'])

                if vacancies:
                    for vacancy in vacancies:
                        salary = vacancy.get('salary', {})
                        if salary:  # Проверка на None
                            vacancy_data = {
                                "employer_id": employer['id'],
                                "vacancy_name": vacancy['name'],
                                "vacancy_url": vacancy['alternate_url'],
                                "salary_from": salary.get('from', 'Не указана'),
                                "salary_to": salary.get('to', 'Не указана'),
                                "currency": salary.get('currency', 'Не указана')
                            }
                            # vacancies_info[vacancy['name']] = vacancy_data
                            vacancies_info.append(vacancy_data)
                        else:
                            vacancy_data = {
                                "employer_id": employer['id'],
                                "vacancy_name": vacancy['name'],
                                "vacancy_url": vacancy['alternate_url'],
                                "salary_from": None,
                                "salary_to": None,
                                "currency": None
                            }
                            # vacancies_info[vacancy['name']] = vacancy_data
                            vacancies_info.append(vacancy_data)

                # else:
                    # print("  Нет доступных вакансий")
                    # None

                employer_with_vacancies = {
                    "Работодатель": employer_data,
                    "Вакансии": vacancies_info
                }

                employer_with_vacancies_list.append(employer_with_vacancies)
        print(employer_with_vacancies_list)
        return employer_with_vacancies_list


if __name__ == "__main__":
    manager = EmployerVacancyManager()
    employer_vacancies = manager.get_vacancies_and_employer()
    print(employer_vacancies)
