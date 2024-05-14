from unittest import TestCase
from api.Yandex import YandexAPI
import requests
import os
from hashlib import sha256
import shutil
import logging
import configparser


class TestYandexApi(TestCase):
    folder_name = 'test_folder'
    file_name = 'test_file.txt'

    @classmethod
    def setUpClass(cls):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        if not config["SERVICE"]["service_type"] == 'YandexDrive':
            exit('В конфиг - файле указан другой тип облачного хранилища')
        cls.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Connection': 'keep-close',
            'Authorization': f'OAuth {config["SERVICE"]["service_token"]}'
        }
        cls.api_path = 'https://cloud-api.yandex.net/v1/disk/resources'
        logging.disable()
        cls.yandex_api = YandexAPI(config['SERVICE']['service_token'], cls.folder_name)
        os.mkdir(cls.folder_name)
        with open(os.path.join(cls.folder_name, cls.file_name), 'w+') as test_file_obj:
            test_file_obj.write('Test text, no more...')

    def test_test_folder_exists(self):
        self.assertTrue(os.path.exists(self.folder_name))

    def test_test_file_exists(self):
        self.assertTrue(os.path.exists(os.path.join(self.folder_name, self.file_name)))

    def test_load(self):
        self.yandex_api.load(os.path.join(self.folder_name, self.file_name), self.file_name)
        result = requests.get(f'{self.api_path}?path={self.folder_name}%2F{self.file_name}',
                              headers=self.headers)
        requests.delete(f'{self.api_path}?path={self.folder_name}%2F{self.file_name}',
                        headers=self.headers)
        self.assertTrue(result.status_code == 200)

    def test_delete(self):
        self.yandex_api.load(os.path.join(self.folder_name, self.file_name), self.file_name)
        self.yandex_api.delete(self.file_name)
        result = requests.get(f'{self.api_path}?path={self.folder_name}%2F{self.file_name}', headers=self.headers)
        self.assertTrue(result.status_code == 404)

    def test_get_info(self):
        result = self.yandex_api.get_info()
        self.assertTrue(len(result.keys()) == 0)

    def test_reload(self):
        self.yandex_api.load(os.path.join(self.folder_name, self.file_name), self.file_name)
        result = requests.get(f'{self.api_path}?path={self.folder_name}%2F{self.file_name}',
                              headers=self.headers).json()
        with open(os.path.join(self.folder_name, self.file_name), 'rb') as test_file_obj:
            old_sha256_machine = sha256(test_file_obj.read()).hexdigest()
        old_sha256 = result['sha256']
        if old_sha256 == old_sha256_machine:
            with open(os.path.join(self.folder_name, self.file_name), 'w+') as test_file_obj:
                test_file_obj.write('New text appended')
            self.yandex_api.reload(os.path.join(self.folder_name, self.file_name), self.file_name)
            new_result = requests.get(f'{self.api_path}?path={self.folder_name}%2F{self.file_name}',
                                      headers=self.headers).json()
            with open(os.path.join(self.folder_name, self.file_name), 'rb') as test_file_obj:
                new_sha256_machine = sha256(test_file_obj.read()).hexdigest()
            self.assertTrue(new_result['sha256'] != old_sha256 and new_sha256_machine == new_result['sha256'])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.folder_name)
        requests.delete(f'{cls.api_path}?path={cls.folder_name}', headers=cls.headers)
