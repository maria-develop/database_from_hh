from typing import Any

import psycopg2


def create_tables(name_base: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения информации о работодателях и вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {name_base}')
    cur.execute(f'CREATE DATABASE {name_base}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=name_base, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                company_url TEXT,
                open_vacancies INTEGER
            );
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES companies(company_id),
                title VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                vacancy_url TEXT
            );
        """)
    conn.commit()
    conn.close()

def insert_company_data(data: list[dict[str, Any]], name_dase: str, params: dict) -> None:
    """Сохранение данных о компаниях и их вакансиях в базу данных "hh_base"."""
    conn = psycopg2.connect(dbname=name_dase, **params)
    with conn.cursor() as cur:
        for company in data:
            company_id = company['Работодатель']['id']
            company_name = company['Работодатель']['employer_name']
            company_url = company['Работодатель']['alternate_url']
            open_vacancies = company['Работодатель']['open_vacancies']
            cur.execute("""
                INSERT INTO companies (company_id, company_name, company_url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                RETURNING company_id; 
            """, (company_id, company_name, company_url, open_vacancies))

            company_id = cur.fetchone()[0]
            vacancies_data = company['Вакансии']
            for vacancy in vacancies_data:
                vacancy_name = vacancy['vacancy_name']
                vacancy_url = vacancy['vacancy_url']
                salary = f'{vacancy['salary_from']} - {vacancy['salary_to']} {vacancy['currency']}'
                salary_from = vacancy['salary_from']
                salary_to = vacancy['salary_to']
                cur.execute("""
                            INSERT INTO vacancies (company_id, title, vacancy_url, salary_from, salary_to)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING company_id; 
                        """, (company_id, vacancy_name, vacancy_url, salary_from, salary_to))

    conn.commit()
    conn.close()
