from unittest.mock import patch


@patch('src.hh_api.requests.get')
def test_get_employers_by_name(mock_get, employer_vacancy_manager):
    """Тест для метода get_employers_by_name с использованием mock."""
    mock_get.return_value.json.return_value = {
        "items": [
            {"id": "1", "name": "Test Company", "alternate_url": "http://test.com", "open_vacancies": 5}
        ]
    }
    employers = employer_vacancy_manager.get_employers_by_name("Test Company")
    assert len(employers) == 1
    assert employers[0]['name'] == "Test Company"


@patch('src.hh_api.requests.get')
def test_get_vacancies_by_employer(mock_get, employer_vacancy_manager):
    """Тест для метода get_vacancies_by_employer с использованием mock."""
    mock_get.return_value.json.return_value = {
        "items": [
            {"id": "1", "name": "Test Vacancy", "alternate_url": "http://test.com/vacancy", "salary": {"from": 50000, "to": 100000}}
        ]
    }
    vacancies = employer_vacancy_manager.get_vacancies_by_employer("1")
    assert len(vacancies) == 1
    assert vacancies[0]['name'] == "Test Vacancy"
