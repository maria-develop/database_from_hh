import psycopg2

from typing import Any
from config import config
from src.db_manager_abstract import DBManagerABC


class DBManager(DBManagerABC):
    """Подключение к базе данных и реализация методов для получения данных"""
    def __init__(self, dbname='postgres'):
        # Получаем параметры подключения из файла конфигурации
        params = config()
        params['dbname'] = dbname  # добавляем имя базы данных в параметры

        try:
            # Пытаемся подключиться к базе данных
            self.connection = psycopg2.connect(**params)
            self.connection.autocommit = True
            # print("Соединение с базой данных успешно установлено.")
        except psycopg2.OperationalError:
            # print(f"Ошибка подключения к базе данных: {e}")
            self.connection = None

    def __del__(self):
        # Закрытие соединения при удалении объекта
        if self.connection:
            self.connection.close()
            # print("Соединение с базой данных закрыто.")

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Список кортежей (название компании, количество вакансий)
        """
        with self.connection.cursor() as cur:
            cur.execute("""
                    SELECT company_name, open_vacancies
                    FROM companies;
                """)
            result = cur.fetchall()
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с названием компании, названия вакансии, зарплаты и ссылки на вакансию."""
        with self.connection.cursor() as cur:
            cur.execute("""
                    SELECT companies.company_name, vacancies.title,
                    vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url
                    FROM vacancies
                    JOIN companies ON vacancies.company_id = companies.company_id;
                """)
            result = cur.fetchall()
        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        with self.connection.cursor() as cur:
            cur.execute("""
                    SELECT AVG((salary_from + salary_to) / 2.0)
                    FROM vacancies
                    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
                """)
            avg_salary_ = cur.fetchone()[0]
        return avg_salary_

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary_ = self.get_avg_salary()
        with self.connection.cursor() as cur:
            cur.execute("""
                    SELECT companies.company_name, vacancies.title, vacancies.salary_from,
                    vacancies.salary_to, vacancies.vacancy_url
                    FROM vacancies
                    JOIN companies ON vacancies.company_id = companies.company_id
                    WHERE (salary_from + salary_to) / 2.0 > (
        SELECT AVG((salary_from + salary_to) / 2.0)
        FROM vacancies
    );
                """, (avg_salary_,))
            result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        with self.connection.cursor() as cur:
            # Используем форматирование строки для LIKE
            search_pattern = f"%{keyword}%"

            # Выполнение SQL-запроса
            cur.execute(f"""
                SELECT companies.company_name, vacancies.title,
                vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
                WHERE vacancies.title LIKE '{search_pattern}';
            """)

            result = cur.fetchall()
        return result


# Пример использования:
if __name__ == "__main__":
    db_manager = DBManager(dbname='hh_base')

    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    print("Компании и количество вакансий:", companies_and_vacancies)

    all_vacancies = db_manager.get_all_vacancies()
    print("Все вакансии:", all_vacancies)

    avg_salary = db_manager.get_avg_salary()
    print("Средняя зарплата:", avg_salary)

    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print("Вакансии с зарплатой выше средней:", higher_salary_vacancies)

    python_vacancies = db_manager.get_vacancies_with_keyword('экономист')
    print("Вакансии с ключевым словом 'экономист':", python_vacancies)
