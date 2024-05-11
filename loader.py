import os
from exceptions.SystemExceptions import InIEmptyError
import configparser


def load_start_data():
    try:
        if not os.path.exists('config.ini'):
            raise InIEmptyError
    except InIEmptyError as ex:
        exit(f'Невозможно начать работу: {ex}')
    else:
        config = configparser.ConfigParser()
        config_data = config.read('config.ini')
        return config_data


load_start_data()

