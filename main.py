from src.db_manager import DBManager
from src.hh_api import EmployerVacancyManager
from src.base import create_tables, insert_company_data
from config import config


def main():
    params = config()

    data = EmployerVacancyManager()
    create_tables('hh_base', params)
    insert_company_data(data, "hh_base", params)

    db_manager = DBManager(dbname='hh_base')
    db_manager.get_companies_and_vacancies_count()
    db_manager.get_all_vacancies()
    db_manager.get_avg_salary()
    db_manager.get_vacancies_with_higher_salary()
    db_manager.get_vacancies_with_keyword('экономист')


if __name__ == '__main__':
    main()
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
