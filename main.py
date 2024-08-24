from db_manager import DBManager
from hh_api import get_vacancies_and_employer
from base import create_tables, insert_company_data
from config import config


def main():
    params = config()

    data = get_vacancies_and_employer()
    create_tables('hh_base', params)
    insert_company_data(data, "hh_base", params)
    # db_manager = DBManager(dbname='hh_base')
    # db_manager.get_companies_and_vacancies_count()
    # db_manager.get_all_vacancies()
    # db_manager.get_avg_salary()
    # db_manager.get_vacancies_with_higher_salary()
    # db_manager.get_vacancies_with_keyword('экономист')


if __name__ == '__main__':
    main()
