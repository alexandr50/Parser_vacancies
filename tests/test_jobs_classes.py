import pytest
from classes.jobs_classes import HHVacancy, SJVacancy, sorting, get_top


@pytest.fixture
def vacancy_hh():
    return HHVacancy('Python Developer', 'от 500000 до 1000000', 'Description', 'Sky_Pro', 'https://hh.sky.pro/', 'от 3 до 6 лет')

@pytest.fixture
def vacancy_sj():
    return SJVacancy('Java', 'от 100000 до 300000', 'Работа с бд', 'Tesla', 'https://superjob.ru/vacancy/78127418', 'от 1 года до 3 лет')

def test_init_hh(vacancy_hh):
    assert vacancy_hh.name == 'Python Developer'
    assert vacancy_hh.salary == 'от 500000 до 1000000'
    assert vacancy_hh.description == 'Description'
    assert vacancy_hh.company_name == 'Sky_Pro'
    assert vacancy_hh.url == 'https://hh.sky.pro/'
    assert vacancy_hh.experience == 'от 3 до 6 лет'
    assert vacancy_hh.__str__() == f'HH: Sky_Pro, зарплата: от 500000 до 1000000 руб/мес, ссылка: https://hh.sky.pro/, тебуемый опыт: от 3 до 6 лет, описание: Description'

def test_compare(vacancy_hh):
    vacancy_hh_2 = HHVacancy('Python Developer2', 'от 200000 до 500000', 'Description2', 'Sky_Pro2', 'https://hh.sky.pro_pro/', 'от 1 года до 3 лет')
    assert vacancy_hh > vacancy_hh_2
    with pytest.raises(TypeError):
        assert vacancy_hh > 2
    assert vacancy_hh_2 < vacancy_hh
    with pytest.raises(TypeError):
        assert vacancy_hh_2 < '9'

def test_init_sj(vacancy_sj):
    assert vacancy_sj.name == 'Java'
    assert vacancy_sj.salary == 'от 100000 до 300000'
    assert vacancy_sj.description == 'Работа с бд'
    assert vacancy_sj.company_name == 'Tesla'
    assert vacancy_sj.url == 'https://superjob.ru/vacancy/78127418'
    assert vacancy_sj.experience == 'от 1 года до 3 лет'
    assert vacancy_sj.__str__() == f'SJ: Tesla, зарплата: от 100000 до 300000 руб/мес, ссылка: https://superjob.ru/vacancy/78127418, тебуемый опыт: от 1 года до 3 лет, описание: Работа с бд'


def test_sorted(vacancy_hh, vacancy_sj):
    vacancy_hh_2 = HHVacancy('Python Developer2', 'от 350000', 'Description2', 'Sky_Pro2','https://hh.sky.pro_pro/', 'от 1 года до 3 лет')
    vacancy_sj_2 = SJVacancy('Python', 'не указана', 'some_escription', 'X-Space', 'https://superjob.x_space/', 'от 1 года до 3 лет')
    list_before_sorting = [vacancy_hh, vacancy_hh_2, vacancy_sj, vacancy_sj_2]
    list_after_sorting = [vacancy_sj_2, vacancy_sj, vacancy_hh_2, vacancy_hh]
    assert sorting(list_before_sorting) == list_after_sorting
    assert get_top(list_after_sorting, 2) == [vacancy_hh_2, vacancy_hh]
