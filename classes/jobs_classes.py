from pathlib import Path

from utils.utils import get_hh_from_url, get_superjob_from_url

path = Path('file.json')


class Vacancy:
    __slots__ = ('name', 'salary', 'description', 'company_name', 'url', 'experience')


    def __init__(self, name: str, salary: str, description: str, company_name: str, url: str, experience: str):
        self.name = name
        self.salary = salary
        self.description = description
        self.company_name = company_name
        self.url = url
        self.experience = experience

    @staticmethod
    def get_int_salary(salary: str) -> int:
        if salary.lower() == 'не указана':
            return 0
        elif len(salary.split(' ')) == 4:
            return int(salary.split(' ')[3])
        else:
            return int(salary.split(' ')[1])

    def __lt__(self, other):
        if type(other) not in (HHVacancy, SJVacancy):
            raise TypeError('Аргумент должен быть типом HHVacancy или SJVacancy')
        else:
            return self.get_int_salary(self.salary) < self.get_int_salary(other.salary)

    def __gt__(self, other):
        if type(other) not in (HHVacancy, SJVacancy):
            raise TypeError('Аргумент должен быть типом HHVacancy или SJVacancy')
        else:
            return self.get_int_salary(self.salary) > self.get_int_salary(other.salary)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.company_name}, {self.url}, {self.description}, {self.salary}, {self.experience})'


class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """

    def __init__(self, name: str, salary: str, description: str, company_name: str, url: str, experience: str):
        if get_hh_from_url(url):
            super().__init__(name, salary, description, company_name, url, experience)

    def __str__(self):
        return f'HH: {self.company_name}, зарплата: {self.salary} руб/мес, ссылка: {self.url}, тебуемый опыт: {self.experience}, описание: {self.description[:50]}'


class SJVacancy(Vacancy):  # add counter mixin
    def __init__(self, name: str, salary: str, description: str, company_name: str, url: str, experience: str):
        if get_superjob_from_url(url):
            super().__init__(name, salary, description, company_name, url, experience)

    def __str__(self):
        return f'SJ: {self.company_name}, зарплата: {self.salary} руб/мес, ссылка: {self.url}, тебуемый опыт: {self.experience}, описание: {self.description[:50]}'


def sorting(vacancies: list):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    for i in range(len(vacancies)):
        min = i
        for j in range(i + 1, len(vacancies)):
            if vacancies[j] < vacancies[min]:
                min = j
        vacancies[min], vacancies[i] = vacancies[i], vacancies[min]
    return vacancies


def get_top(vacancies: list, top_count: int):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    res = sorting(vacancies)[top_count * -1:]
    return res


