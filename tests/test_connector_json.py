import pytest

from classes.connector import ConnectorJson


@pytest.fixture
def connector_json():
    return ConnectorJson('test.json')


def test_init(connector_json):
    assert connector_json.data_file == 'test.json'


def test_insert(connector_json):
    del connector_json.data_file
    data = {
        "name": "Алго Дилер",
        "salary": "Не указана",
        "description": "description",
        "company_name": "Держава , АКБ",
        "url": "https://hh.ru/vacancy/77659165",
        "experience": "Без опыта"
    }
    connector_json.insert(data)
    result = connector_json.select({})
    assert result == [data]


def test_setter(connector_json):
    connector_json.data_file = 'test_file.json'
    assert connector_json.data_file == 'test_file.json'


def test_select(connector_json):
    connector_json.data_file = 'test_file.json'
    result = connector_json.select({"name": "Алго Дилер"})
    assert result == [{
        "name": "Алго Дилер",
        "salary": "Не указана",
        "description": "description",
        "company_name": "Держава , АКБ",
        "url": "https://hh.ru/vacancy/77659165",
        "experience": "Без опыта"
    }]
    result = connector_json.select_for_keyword('keyword')
    assert result == [{
        "name": "Алго Дилер2",
        "salary": "Не указана2",
        "description": "description2 keyword",
        "company_name": "Держава , АКБ2",
        "url": "https://hh.ru/vacancy/776591652",
        "experience": "Без опыта2"
    }]


def test_delete(connector_json):
    result = connector_json.delete({"name": "Алго Дилер"})
    assert result == []
