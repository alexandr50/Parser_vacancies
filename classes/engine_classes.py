import os
from abc import ABC, abstractmethod
import re
import requests
from dotenv import load_dotenv
from pydantic import ValidationError

from classes.connector import ConnectorJson
from utils.utils import get_correct_sj_salary, correct_hh_salary, get_correct_experience_sj
from pathlib import Path

from validator import VacancyApi

path = Path('file.json')

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')  # Загружаю файл с ключом аутентификации для superjob
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SUPERJOB_KEY = os.environ.get('SUPERJOB_KEY')  # Получаю ключ


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = ConnectorJson(file_name)
        return connector


class HH(Engine):

    def get_request(self, name_vacancy: str = 'python'):
        """ Функция обращается к апи и записывает в файл информацию по всем вакансиям по ключевому слову в формате json """

        self.name_vacancy = name_vacancy
        self.experience = [{'noExperience': 'Без опыта'}, {'between1And3': 'От 1 года до 3 лет'},
                           # в запросе буду подставлять разные опыты работы
                           {'between3And6': 'От 3 до 6 лет'}, {'moreThan6': 'Более 6 лет'}]
        self.url = f'https://api.hh.ru/vacancies/?text={self.name_vacancy}'

        for i in range(1, 16):

            data_dict = {}
            response = requests.get(self.url, params={'User-Agent': 'Mozilla/4.0',
                                                      'area': '113',
                                                      'experience': {
                                                          *self.experience[i // len(self.experience)].keys()},
                                                      'per_page': '63',
                                                      'page': str(i)})
            if response.status_code == 200:

                for item in response.json()['items']:
                    data_dict['name'] = item.get('name')
                    salary = item.get('salary')
                    if salary:
                        data_dict['salary'] = correct_hh_salary(str(item['salary'].get('from')),
                                                                str(item['salary'].get('to')))
                    else:
                        data_dict['salary'] = 'Не указана'
                    data_dict['description'] = re.sub(r'<[^>]*>', ' ', str(item['snippet']['requirement']))
                    data_dict['company_name'] = item['employer'].get('name')
                    data_dict['url'] = item.get('alternate_url')
                    data_dict['experience'] = self.experience[i // len(self.experience)].get(
                        *self.experience[i // len(self.experience)].keys())

                    """ Валидация словаря согласно модели с файле validator.py"""
                    try:
                        VacancyApi(**data_dict)
                    except ValidationError as e:
                        print(e.errors())

                    self.get_connector(path).insert(data_dict)


class SuperJob(Engine):
    """ Функция обращается к апи и записывает в файл информацию по всем вакансиям по ключевому слову в формате json """

    def get_request(self, name_vacancy: str = 'python'):
        self.name_vacancy = name_vacancy
        self.url = f'https://api.superjob.ru/2.0/vacancies/?keyword={self.name_vacancy}&count=50'

        headers = {
            'X-Api-App-Id': SUPERJOB_KEY,
        }

        for i in range(1, 21):
            data_dict = {}
            response = requests.get(f'{self.url}&page={i}', headers=headers)
            if response.status_code == 200:
                for item in response.json()['objects']:
                    data_dict['name'] = item['profession']
                    data_dict['salary'] = get_correct_sj_salary(str(item['payment_from']), str(item['payment_to']))
                    data_dict['description'] = ''.join(re.sub(r'\<[^>]*\>', ' ', item['vacancyRichText']).split(
                        '\n'))  # удаляю html разметку из описания вакансии
                    data_dict['company_name'] = item['firm_name']
                    data_dict['url'] = item['link']
                    data_dict['experience'] = get_correct_experience_sj(item['experience']['title'])

                    """ Валидация словаря согласно модели с файле validator.py"""
                    try:
                        VacancyApi(**data_dict)
                    except ValidationError as e:
                        print(e.errors())

                    self.get_connector(path).insert(data_dict)
