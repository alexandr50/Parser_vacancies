import pytest
from utils.utils import *


@pytest.fixture
def full_salary_hh():
    value_form = '25000'
    value_to = '70000'
    return value_form, value_to


@pytest.fixture
def second_half_salary_hh():
    value_form = 'None'
    value_to = '70000'
    return value_form, value_to


@pytest.fixture
def first_half_salary_hh():
    value_form = '25000'
    value_to = 'None'
    return value_form, value_to


def test_correct_salary_hh_full(full_salary_hh):
    assert correct_hh_salary(*full_salary_hh) == 'от 25000 до 70000'


def test_correct_salary_hh_second_half(second_half_salary_hh):
    assert correct_hh_salary(*second_half_salary_hh) == 'до 70000'


def test_correct_salary_first_half(first_half_salary_hh):
    assert correct_hh_salary(*first_half_salary_hh) == 'от 25000'


def test_correct_salary_sj_full():
    assert get_correct_sj_salary('200000', '300000') == 'от 200000 до 300000'

def test_correct_salary_sj_second_half():
    assert get_correct_sj_salary('0', '300000') == 'до 300000'

def test_correct_salary_sj_first():
    assert get_correct_sj_salary('200000', '0') == 'от 200000 '


def test_correct_salary_sj_empty():
    assert get_correct_sj_salary('0', '0') == 'не указана'


def test_correct_experience_sj():
    assert get_correct_experience_sj('От 3 лет') == 'От 3 до 6 лет'
    assert get_correct_experience_sj('От 1 года') == 'От 1 года до 3 лет'
    assert get_correct_experience_sj('не указана') == 'Без опыта'