import sys
from classes.engine_classes import HH, SuperJob


def select_service():
    """ Функция выбора сервисов для сбора вакансий """

    list_services = ['1', '2', '3']
    select_service_input = input('''Выберите номер сервиса для сбора данных: 1. HeadHunter
                                         2. SuperJob
                                         3. Оба сервиса 
                                         0. Выход: ''')
    if select_service_input == '0':
        sys.exit()
    elif select_service_input not in list_services:
        print('Некорректное значение')
        return select_service()
    else:
        return select_service_input


def select_keyword():
    """ Функция для выбора ключевого слова в запросе к апи """

    dict_keyword = {'1': 'Python developer', '2': 'Django', '3': 'Sql', '4': 'Java'}
    input_keyword = input('''Введите номер ключевого слова: 1. python
                               2. django 
                               3. sql 
                               4. Java
                               0. Выход: ''')
    if input_keyword == '0':
        sys.exit()
    elif input_keyword not in dict_keyword.keys():
        print('Некорректное значение')
        return select_keyword()

    return dict_keyword[input_keyword]


def create_request(number_service, keyword):
    """ Функция выполнения сбора информации в соответствии выбора пользователя"""
    if number_service == '1':
        headhunter = HH()
        headhunter.get_request(keyword)
    elif number_service == '2':
        superjob = SuperJob()
        superjob.get_request(keyword)
    else:
        headhunter = HH()
        headhunter.get_request(keyword)
        superjob = SuperJob()
        superjob.get_request(keyword)

def select_experience():
    """ Функция фильтрации данных по опыту работы"""
    dict_experience = {'1': 'Без опыта', '2': 'От 1 года до 3 лет', '3': 'От 3 до 6 лет', '4': 'От 6 лет'}
    user_input = input('''Выберите номер для фильтрации: 1. Без опыта
                               2. От 1 года до 3 лет
                               3. От 3 до 6 лет
                               4. От 6 лет
                               0. Выход: ''')
    if user_input == '0':
        sys.exit()
    elif user_input not in dict_experience.keys():
        print('Некорректное значение')
        return select_experience()
    else:
        return dict_experience[user_input]



