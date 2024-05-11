from api.CloudServiceAbstract import CloudService
import requests
from exceptions.cloud_services.YandexExceptions import check_answer
import logging


class YandexAPI(CloudService):
    def __init__(self, token, folder):
        self._token = token
        self._service_folder = folder
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Connection': 'keep-close',
            'Authorization': f'OAuth {self._token}'
        }
        self._file_path = 'https://cloud-api.yandex.net/v1/disk/resources'
        self._full_format = '%Y-%m-%dT%H:%M:%S%z'

    def __check_or_create_folder(self):
        try:
            is_exist = requests.get(f'{self._file_path}?path={self._service_folder}', headers=self._headers)
            if is_exist.status_code == 404:
                result = requests.put(f'{self._file_path}?path={self._service_folder}', headers=self._headers)
                check_answer(result.status_code)
        except Exception as ex:
            logging.error(f'Не удалось создать папку {self._service_folder}: ошибка: {ex}')
        else:
            if not is_exist.status_code == 200:
                logging.info(f'Папка {self._service_folder} успешно создана')

    def load(self, path_to_file: str, file_name: str):
        try:
            result = requests.get(f'{self._file_path}/upload?path={self._service_folder}%2F{file_name}',
                                  headers=self._headers)
            check_answer(result.status_code)
            result_data = result.json()
            with open(path_to_file, 'rb') as f:
                requests.put(result_data['href'], files={'file': f}, headers=self._headers)
        except Exception as ex:
            logging.error(f'Не удалось загрузить файл {file_name}: ошибка: {ex}')
        else:
            logging.info(f'Файл {file_name} успешно загружен')

    def reload(self, file_path, file_name):
        try:
            delete_result = requests.delete(f'{self._file_path}?path={self._service_folder}%2F{file_name}',
                                            headers=self._headers)
            check_answer(delete_result.status_code)
            result = requests.get(f'{self._file_path}/upload?path={self._service_folder}%2F{file_name}',
                                  headers=self._headers)
            check_answer(result.status_code)
            result_data = result.json()
            with open(file_path, 'rb') as f:
                requests.put(result_data['href'], files={'file': f}, headers=self._headers)
        except Exception as ex:
            logging.error(f'Не удалось обновить файл {file_name}, ошибка: {ex}')
        else:
            logging.info(f'Файл {file_name} успешно обновлен')

    def delete(self, file_path: str):
        try:
            result = requests.delete(f'{self._file_path}?path={self._service_folder}%2F{file_path}',
                                     headers=self._headers)
            check_answer(result.status_code)
        except Exception as ex:
            logging.error(f'Не удалось удалить файл {file_path}: ошибка:{ex}')
        else:
            logging.info(f'Файл {file_path} успешно удален из хранилища')

    def get_info(self):
        try:
            self.__check_or_create_folder()
            result = requests.get(f'{self._file_path}?path={self._service_folder}%2F',
                                  headers=self._headers)
            check_answer(result.status_code)
            data = dict()
            for item in result.json()['_embedded']['items']:
                data.setdefault(item['name'], {'sha256': item['sha256']})
        except Exception as ex:
            logging.error(f'Не удалось получить информацию о файлах: ошибка: {ex}')
        else:
            return data
