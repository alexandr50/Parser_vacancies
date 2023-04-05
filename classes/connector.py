import json
import os

from pydantic import ValidationError

from validator import VacancyApi

from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class ConnectorJson(BaseConnector):
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """

    def __init__(self, data_file: str):
        self.__connect(data_file)
        self.__data_file = data_file

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, data_file: str):
        self.__connect(data_file)
        self.__data_file = data_file

    @data_file.deleter
    def data_file(self):
        """ Метод удаления данных из файла """
        with open(self.data_file, 'w') as file:
            json.dump([], file)

    def __connect(self, data_file: str):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """

        if not os.path.exists(data_file):
            with open(data_file, 'w') as file:
                json.dump([], file, indent=4)
        elif os.path.exists(data_file) and os.stat(data_file).st_size != 0:
            with open(data_file, 'r') as file:
                result_list = json.load(file)
                for item in result_list:
                    try:
                        VacancyApi(**item)
                    except ValidationError as e:
                        print(e.errors())
        else:
            return True

    def insert(self, data: dict):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.data_file, 'r') as file:
            res = json.load(file)
            res.append(data)
            with open(self.data_file, 'w') as file:
                json.dump(res, file, indent=4, ensure_ascii=False)

    def select(self, query: dict) -> list:
        """Метод выборки данных из файла по переданному в него словарю"""

        with open(self.data_file, 'r') as file:
            data_file: list = json.load(file)
            if not query:
                return data_file
            else:
                key, value = *query.keys(), *query.values()
                result_data_file = list(filter(lambda x: x[key] == value, data_file))
        return result_data_file

    def delete(self, query: dict):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        with open(self.data_file, 'r') as file:
            data_file: list = json.load(file)
            if query:
                key, value = *query.keys(), *query.values()
                result = list(filter(lambda x: x[key] == value, data_file))
                for item in result:
                    data_file.remove(item)
                with open(self.data_file, 'w') as fl:
                    json.dump(data_file, fl, indent=4, ensure_ascii=False)
        return data_file

    def select_for_keyword(self, keyword: str) -> list:
        """ Функция поиска ключевого слова в описании вакансии """
        result_list = []
        with open(self.data_file, 'r') as file:
            data_file: list = json.load(file)
            for item in data_file:
                if keyword in item['description']:
                    result_list.append(item)
        return result_list
