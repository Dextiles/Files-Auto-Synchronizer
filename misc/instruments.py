from exceptions.SystemExceptions import *
import configparser
import os
from api.Yandex import YandexAPI


def load_config():
    try:
        if not os.path.exists('config.ini'):
            raise InIEmptyError
        else:
            cfg = configparser.ConfigParser()
            with open('config.ini') as cf:
                cfg.read_file(cf)
                if not cfg.has_section('PARAMS') or not cfg.has_section('SERVICE'):
                    raise NotGoodINIError
                else:
                    params = cfg.options('PARAMS')
                    service = cfg.options('SERVICE')
                    if 'local_folder' not in params and 'service_folder' not in params and 'sync_interval' not in params:
                        raise NotGoodINIError
                    elif 'service_token' not in service and 'service_type' not in service:
                        raise NotGoodINIError
    except Exception as ex:
        exit(f'Невозможно начать работу: {ex}')
    else:
        return cfg


def check_directory(directory):
    try:
        if not os.path.exists(directory):
            raise NotExistsDirectoryError(directory)
    except Exception as ex:
        exit(f'Невозможно начать работу: {ex}')


def check_cloud_service_config(service_id):
    try:
        if service_id == 'YandexDrive':
            return YandexAPI
        else:
            raise NotGoodINIError
    except Exception as ex:
        exit(f'Невозможно начать работу: {ex}')